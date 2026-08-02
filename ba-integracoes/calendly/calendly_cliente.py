#!/usr/bin/env python3
"""
Cliente Calendly — eventos agendados, cancelados, resumo.

Uso CLI:
    python calendly_cliente.py hoje
    python calendly_cliente.py amanha
    python calendly_cliente.py resumo-semana
    python calendly_cliente.py cancelados 7

Credenciais:
    CALENDLY_TOKEN=eyJ...
    CALENDLY_USER_URI=https://api.calendly.com/users/SEU_ID

"""
from __future__ import annotations

import json
import os
import sys
from datetime import date, datetime, timedelta, timezone

try:
    import requests
except ImportError:
    sys.exit("erro: instale 'requests' (pip install requests)")


BASE = "https://api.calendly.com"


class CalendlyCliente:
    def __init__(self, token: str | None = None, user_uri: str | None = None, timeout: int = 30):
        self.token = token or os.environ.get("CALENDLY_TOKEN", "")
        self.user_uri = user_uri or os.environ.get("CALENDLY_USER_URI", "")
        if not self.token or not self.user_uri:
            sys.exit("erro: defina CALENDLY_TOKEN e CALENDLY_USER_URI")
        self.timeout = timeout

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}

    def _get(self, url: str, params: dict | None = None) -> dict:
        if not url.startswith("http"):
            url = f"{BASE}{url}"
        r = requests.get(url, headers=self._headers(), params=params or {}, timeout=self.timeout)
        if not r.ok:
            raise RuntimeError(f"Calendly {r.status_code}: {r.text}")
        return r.json()

    def _delete(self, url: str, data: dict | None = None) -> dict:
        r = requests.post(
            f"{url}/cancellation" if not url.endswith("/cancellation") else url,
            headers={**self._headers(), "Content-Type": "application/json"},
            data=json.dumps(data or {}),
            timeout=self.timeout,
        )
        if not r.ok:
            raise RuntimeError(f"Calendly {r.status_code}: {r.text}")
        return r.json()

    # ------------------------------------------------------------- eventos
    def _to_evento(self, e: dict) -> dict:
        return {
            "uri": e["uri"],
            "titulo": e.get("name") or "",
            "status": e.get("status"),  # active | canceled
            "inicio": e["start_time"],
            "fim": e["end_time"],
            "tipo_uri": e.get("event_type"),
            "criado_em": e.get("created_at"),
            "cancelado": e.get("status") == "canceled",
            "motivo_cancelamento": (e.get("cancellation") or {}).get("reason"),
        }

    def eventos_por_periodo(
        self,
        inicio: datetime,
        fim: datetime,
        status: str | None = None,
    ) -> list[dict]:
        params = {
            "user": self.user_uri,
            "min_start_time": inicio.isoformat().replace("+00:00", "Z"),
            "max_start_time": fim.isoformat().replace("+00:00", "Z"),
            "count": 100,
        }
        if status:
            params["status"] = status

        eventos: list[dict] = []
        url: str | None = f"{BASE}/scheduled_events"
        while url:
            j = self._get(url, params if url == f"{BASE}/scheduled_events" else None)
            for e in j.get("collection", []):
                eventos.append(self._to_evento(e))
            url = ((j.get("pagination") or {}).get("next_page"))
        # ordena por inicio
        eventos.sort(key=lambda e: e["inicio"])
        # enriquece com convidado
        for e in eventos:
            e.update(self._convidados(e["uri"]))
        return eventos

    def _convidados(self, evento_uri: str) -> dict:
        j = self._get(f"{evento_uri}/invitees")
        invitees = j.get("collection", [])
        if not invitees:
            return {"convidado_nome": "", "convidado_email": "", "questoes": []}
        inv = invitees[0]
        return {
            "convidado_nome": inv.get("name") or "",
            "convidado_email": inv.get("email") or "",
            "questoes": [
                {"pergunta": q.get("question"), "resposta": q.get("answer")}
                for q in inv.get("questions_and_answers", [])
            ],
        }

    def eventos_hoje(self) -> list[dict]:
        agora = datetime.now(timezone.utc)
        inicio_dia = agora.replace(hour=0, minute=0, second=0, microsecond=0)
        fim_dia = inicio_dia + timedelta(days=1, seconds=-1)
        return self.eventos_por_periodo(inicio_dia, fim_dia, status="active")

    def eventos_amanha(self) -> list[dict]:
        agora = datetime.now(timezone.utc)
        inicio = agora.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        fim = inicio + timedelta(days=1, seconds=-1)
        return self.eventos_por_periodo(inicio, fim, status="active")

    def eventos_cancelados_recentes(self, dias: int = 7) -> list[dict]:
        agora = datetime.now(timezone.utc)
        return self.eventos_por_periodo(agora - timedelta(days=dias), agora, status="canceled")

    def evento_detalhe(self, uri: str) -> dict:
        e = self._get(uri).get("resource", {})
        det = self._to_evento(e)
        det.update(self._convidados(uri))
        return det

    def cancelar_evento(self, uri: str, motivo: str) -> dict:
        return self._delete(f"{uri}/cancellation", {"reason": motivo})

    # -------------------------------------------------------------- resumo
    def resumo_semana(self) -> dict:
        agora = datetime.now(timezone.utc)
        inicio = agora - timedelta(days=agora.weekday())  # segunda da semana atual
        inicio = inicio.replace(hour=0, minute=0, second=0, microsecond=0)
        fim = inicio + timedelta(days=7, seconds=-1)

        ativos = self.eventos_por_periodo(inicio, fim, status="active")
        cancelados = self.eventos_por_periodo(inicio, fim, status="canceled")
        return {
            "periodo": f"{inicio.date()} a {fim.date()}",
            "ativos": len(ativos),
            "cancelados": len(cancelados),
            "taxa_cancelamento_pct": round(
                len(cancelados) / max(len(ativos) + len(cancelados), 1) * 100, 1
            ),
            "proximos_3": ativos[:3],
        }


# ------------------------------------------------------------------- CLI
def _print_json(obj) -> None:
    print(json.dumps(obj, default=str, indent=2, ensure_ascii=False))


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("uso: calendly_cliente.py <hoje | amanha | resumo-semana | cancelados [N]>")
    cmd = sys.argv[1]
    c = CalendlyCliente()
    if cmd == "hoje":
        _print_json(c.eventos_hoje())
    elif cmd == "amanha":
        _print_json(c.eventos_amanha())
    elif cmd == "resumo-semana":
        _print_json(c.resumo_semana())
    elif cmd == "cancelados":
        dias = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        _print_json(c.eventos_cancelados_recentes(dias))
    else:
        sys.exit(f"comando desconhecido: {cmd}")


if __name__ == "__main__":
    main()
