"""Kafka consumers for auth-service.

One handler per subscribed topic. Handlers are best-effort logging plus
audit — services override this file to implement real cross-domain behavior.
"""
from __future__ import annotations

import logging

from healthcare_common.audit import emit_audit

log = logging.getLogger("auth-service.consumers")


def register(svc) -> None:
    bus = svc.bus

    @bus.on("identity.user.deactivated")
    def _on_identity_user_deactivated(envelope: dict) -> None:
        log.info("auth-service: received identity.user.deactivated id=%s", envelope.get("id"))
        emit_audit(bus, action="consume.identity.user.deactivated", actor="system:auth-service",
                   target=None, details={"envelope_id": envelope.get("id")})

