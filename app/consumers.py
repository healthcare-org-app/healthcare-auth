"""Kafka consumers for auth-service.

One handler per subscribed topic. Real handlers write to this service's own
database and/or publish follow-up events; stub handlers just log + audit.
"""
from __future__ import annotations

import logging

from psycopg.types.json import Json

from healthcare_common.audit import emit_audit

log = logging.getLogger("auth-service.consumers")

TABLE = "auth"


def register(svc) -> None:
    bus = svc.bus
    db = svc.db
    clients = svc.clients

    @bus.on("identity.user.deactivated")
    def _on_identity_user_deactivated(envelope: dict) -> None:
        data = envelope.get("data") or {}
        try:
                    # Revoke any active sessions.
                    sub = data.get("sub")
                    if not sub: return
                    db.execute(f"UPDATE {TABLE} SET status='revoked', updated_at=now() "
                               f"WHERE data->>'sub' = %s AND status='active'", (str(sub),))
        except Exception as e:
            log.exception("auth-service/identity.user.deactivated handler failed: %s", e)
        emit_audit(bus, action="consume.identity.user.deactivated", actor="system:auth-service",
                   target=None, details={"envelope_id": envelope.get("id")})

