# Beyond Redline — Arquitectura defensiva

> **Estado:** diseño inicial; no describe una infraestructura desplegada ni agentes ya implementados.  
> **Objetivo:** diseñar una plataforma de ciberdefensa para activos propios o explícitamente autorizados.  
> **Principio no negociable:** detectar, contener, preservar evidencia y avisar; nunca contraatacar ni actuar sobre sistemas de terceros.

## 1. Resumen ejecutivo

Beyond Redline combina telemetría de seguridad, políticas Zero Trust, detección de anomalías, contención controlada, gestión de secretos, honeypots y respuesta forense. La IA ayuda a interpretar señales y recomendar acciones, pero no obtiene autoridad ilimitada sobre la infraestructura.

La primera versión debe ser pequeña y verificable: recibir eventos, normalizarlos, correlacionarlos, dejar una pista de auditoría y presentar alertas a una persona. El aislamiento automático, la revocación masiva y cualquier cambio de rutas deben incorporarse después de probarlos en laboratorio y establecer procedimientos de reversión.

### Principios de diseño

1. **Zero Trust:** cada acceso se autoriza explícitamente según identidad, dispositivo, recurso, contexto y política.
2. **Privilegios mínimos:** cada servicio y agente dispone solo de los permisos que necesita.
3. **Contención proporcional:** preferir acciones reversibles y de alcance limitado antes de medidas disruptivas.
4. **Evidencia verificable:** registrar decisiones y acciones en un registro append-only, con protección contra manipulación.
5. **Supervisión humana:** las acciones con impacto amplio necesitan aprobación humana y/o señales independientes.
6. **Degradación segura:** si la IA, el bus de eventos o el almacenamiento fallan, los controles básicos de red e identidad siguen aplicando políticas seguras.
7. **Ámbito autorizado:** sensores, escaneos, honeypots y automatizaciones se limitan a activos propios o autorizados por escrito.

## 2. Arquitectura lógica

~~~mermaid
flowchart TB
    Internet --> Edge[CDN / Anti-DDoS / WAF]
    Edge --> DMZ[DMZ: reverse proxy y servicios públicos]
    DMZ --> ZT[Gateway de acceso / políticas Zero Trust]
    ZT --> APP[Segmento de aplicaciones y API]
    APP --> DATA[Segmento de datos]
    DMZ -. tráfico aislado .-> HONEY[Honeynet segregada]
    APP --> COL[Colectores de telemetría]
    DATA --> COL
    ZT --> COL
    HONEY --> COL
    COL --> BUS[Bus de eventos]
    BUS --> DET[Motor de detección y correlación]
    DET --> POLICY[Motor de políticas]
    POLICY --> HUMAN[Consola SOC / aprobación humana]
    POLICY --> RESP[Ejecutor de respuesta con permisos limitados]
    RESP --> AUDIT[Registro de auditoría append-only]
    DET --> AUDIT
    HUMAN --> AUDIT
~~~

### Zonas y límites de confianza

| Zona | Contenido | Regla principal |
|---|---|---|
| Edge | CDN, WAF y protección DDoS | Filtrar antes de exponer servicios de origen; la mitigación volumétrica depende también del proveedor. |
| DMZ | Reverse proxies y servicios públicos | Sin acceso directo a la red de datos. |
| Gestión / Zero Trust | Identidad, autorización y acceso administrativo | MFA resistente al phishing cuando sea posible; sesiones de duración limitada. |
| Aplicaciones | APIs y servicios internos | Comunicación permitida por servicio, puerto y propósito. |
| Datos | Bases de datos y almacenamiento | Sin acceso directo desde Internet; credenciales separadas y auditadas. |
| Honeynet | Señuelos deliberadamente aislados | Sin rutas hacia producción ni secretos reales; salida a Internet bloqueada por defecto. |
| Observabilidad | Colectores, bus, detección y auditoría | Acceso restringido, autenticado y monitorizado. |

La segmentación lógica debe reflejarse en reglas reales de firewall, políticas de red y cuentas separadas. Un diagrama o una VLAN por sí solos no constituyen aislamiento suficiente.

## 3. Agentes y límites de autoridad

Los agentes son servicios separados o módulos con identidades y permisos independientes. La IA puede resumir evidencia y proponer una respuesta; el ejecutor determinista comprueba la política antes de aplicar cambios.

| Agente | Responsabilidad | Permisos permitidos | Prohibiciones |
|---|---|---|---|
| **Centinela** | Ingesta, normalización, detección y correlación de eventos. | Lectura de telemetría; creación de alertas. | No bloquea, no revoca credenciales ni cambia configuración. |
| **Guardián** | Ejecutar contención aprobada sobre activos inventariados. | Acciones específicas mediante adaptadores allowlist. | Sin shell arbitraria, sin escalar privilegios, sin actuar fuera del inventario. |
| **Cerrajero** | Gestionar rotación y revocación de secretos afectados. | API de la bóveda para secretos asignados. | No lee secretos en claro si la operación no lo exige; no administra sistemas finales. |
| **Señuelo** | Operar honeypots/honeynet y analizar interacciones dentro de ese entorno. | Gestión limitada de señuelos y lectura de su telemetría. | Sin puente a producción ni captura de datos ajenos fuera del ámbito autorizado. |
| **Forense** | Preservar eventos, metadatos y estado autorizado del incidente. | Lectura y creación de paquetes de evidencia firmados. | No altera la fuente de evidencia ni ejecuta remediaciones. |
| **Mensajero** | Notificar, escalar y mantener el estado de comunicaciones. | Envío a destinos previamente aprobados. | No publica datos sensibles en canales no autorizados ni toma decisiones de contención. |

**Control importante:** dos agentes que consultan el mismo detector no son dos confirmaciones independientes. Para acciones críticas, la corroboración debe proceder de fuentes o mecanismos independientes y tener una regla explícita de decisión.

## 4. Escalado de incidentes

Los niveles representan severidad y respuesta; no implican que todas las amenazas deban atravesarlos en orden.

| Nivel | Criterio orientativo | Respuesta |
|---|---|---|
| **0 — Observación** | Anomalía con baja confianza. | Registrar, enriquecer contexto y observar. |
| **1 — Fricción** | Señales sospechosas repetidas. | Aplicar límites de tasa o retos adicionales solo en servicios compatibles; alertar si persiste. |
| **2 — Sesión** | Actividad hostil con evidencia suficiente. | Invalidar la sesión afectada, exigir reautenticación y avisar al equipo. |
| **3 — Contención** | Compromiso confirmado o riesgo alto. | Aislar el activo o la cuenta afectada, preservar evidencia y rotar únicamente los secretos en riesgo. Aprobación según impacto. |
| **4 — Honeynet** | Una interacción puede dirigirse de forma segura a un señuelo controlado. | Usar únicamente rutas y servicios señuelo diseñados para ese propósito; nunca redirigir tráfico arbitrario a sistemas falsos de forma improvisada. |

### Matriz de autorización recomendada

- **Automático:** registrar, enriquecer, crear alerta y aplicar límites de tasa preaprobados con alcance reducido.
- **Aprobación humana o doble control:** aislar equipos críticos, revocar credenciales compartidas, modificar rutas, bloquear rangos amplios o ejecutar una acción con impacto potencial en clientes.
- **Siempre prohibido:** contraatacar, explotar sistemas de origen, instalar código en terceros, exfiltrar información o ejecutar acciones fuera del inventario autorizado.

Cada acción de contención debe incluir una duración, un identificador de solicitud, un motivo, evidencia asociada y un procedimiento de reversión. Las listas de bloqueo deben tener caducidad y revisión para reducir falsos positivos.

## 5. Registro de auditoría y evidencia

Un log append-only no es automáticamente inmutable. Para aumentar la resistencia a la manipulación:

- Asignar un ID único y secuencia monotónica a cada evento.
- Guardar hora del evento y recepción, actor, acción, recurso, resultado, motivo, severidad y referencias a evidencia.
- Encadenar hashes de eventos y firmar lotes periódicos.
- Replicar los lotes firmados a almacenamiento WORM o equivalente administrado con credenciales separadas.
- Sincronizar relojes y registrar desviaciones.
- Separar los permisos de escritura, lectura, retención y administración.
- No guardar contraseñas, tokens, claves privadas ni cuerpos sensibles innecesarios; redactar y minimizar datos personales.
- Definir retención, acceso, exportación y borrado legalmente exigible antes de producción.

### Esquema lógico inicial

~~~text
audit_event
- event_id             UUID
- sequence_number      BIGINT
- occurred_at          TIMESTAMP WITH TIME ZONE
- received_at          TIMESTAMP WITH TIME ZONE
- actor_type           ENUM(agent, user, service, system)
- actor_id             TEXT
- action               TEXT
- resource_type        TEXT
- resource_id          TEXT
- severity              ENUM(info, low, medium, high, critical)
- decision              ENUM(observed, allowed, denied, proposed, approved, executed, failed, reverted)
- reason_code           TEXT
- correlation_id        UUID
- evidence_refs         JSON
- payload_redacted      JSON
- previous_hash         TEXT
- event_hash            TEXT
- signature_ref         TEXT NULL
~~~

El esquema es conceptual, no una migración SQL lista para producción. La evidencia voluminosa debe guardarse como objetos separados con hash, metadatos de integridad y políticas de retención.

## 6. Contrato de eventos entre componentes

Todos los mensajes internos deben estar versionados, autenticados y validados. Una forma inicial:

~~~json
{
  "schema_version": "1.0",
  "event_id": "uuid",
  "occurred_at": "2026-01-01T12:00:00Z",
  "source": "centinela",
  "event_type": "security.alert.created",
  "severity": "high",
  "confidence": 0.92,
  "asset_id": "asset-123",
  "correlation_id": "uuid",
  "evidence_refs": ["evidence-456"],
  "recommended_action": {
    "type": "revoke_session",
    "target_id": "session-789",
    "requires_approval": true
  }
}
~~~

El ejemplo ilustra el formato, no una alerta real. No se deben incluir secretos en el mensaje. El consumidor valida el esquema, la identidad del emisor, el ámbito del activo y la idempotencia antes de aceptar una solicitud.

### API interna propuesta

| Operación lógica | Entrada | Resultado |
|---|---|---|
| `POST /v1/events` | Evento normalizado | ID de recepción y estado de validación |
| `POST /v1/alerts` | Señales correlacionadas y evidencia | Alerta persistida |
| `POST /v1/actions` | Acción propuesta, alcance, motivo y expiración | Solicitud pendiente de política/aprobación |
| `POST /v1/actions/{id}/approve` | Identidad del aprobador y decisión | Aprobación o rechazo auditado |
| `POST /v1/actions/{id}/execute` | ID de acción aprobada | Resultado del ejecutor; no acepta comandos arbitrarios |
| `GET /v1/incidents/{id}` | ID de incidente | Cronología autorizada y referencias de evidencia |

Estas rutas son un contrato preliminar, no endpoints implementados. La API necesita autenticación servicio-a-servicio, autorización por recurso, límites de tasa, validación estricta, idempotencia y auditoría.

## 7. Flujo de respuesta

1. Un colector recibe telemetría de un activo inventariado.
2. Centinela normaliza el evento y correlaciona señales con contexto de identidad y activo.
3. El motor de políticas determina severidad, confianza y acciones permitidas.
4. Forense preserva los datos pertinentes antes de cambios que puedan destruir evidencia.
5. Si procede, se crea una propuesta de acción con alcance limitado y plazo de expiración.
6. El ejecutor verifica permisos, aprobación, vigencia, idempotencia y estado del activo.
7. Guardián aplica solo la acción allowlist; Cerrajero actúa solo sobre secretos afectados y autorizados.
8. Mensajero comunica la alerta y el resultado al equipo responsable.
9. Se registra cada transición, incluido rechazo, error, reversión y aprobación.
10. El incidente se cierra tras revisión y se documentan falsos positivos y mejoras.

No se debe prometer que una IP identifica a una persona. Direcciones compartidas, VPN, NAT y servicios cloud hacen que el bloqueo por IP/ASN pueda afectar a usuarios legítimos. Las medidas de red deben tener alcance, duración, justificación y mecanismo de revisión.

## 8. Stack: propuesta para evaluar, no decisión cerrada

El documento original deja pendiente escoger stack. Para un MVP mantenible, evaluar estas opciones antes de comprometerse:

- **Agentes y API:** Python con FastAPI para prototipado y ecosistema de análisis; ejecutar tareas privilegiadas en servicios pequeños separados.
- **Políticas:** motor explícito de políticas (por ejemplo, OPA) o reglas deterministas versionadas; la decisión de seguridad no debe depender exclusivamente de una respuesta generativa.
- **Persistencia:** PostgreSQL para inventario, alertas y estado transaccional; almacenamiento de objetos con retención protegida para evidencia.
- **Telemetría:** OpenTelemetry y colectores compatibles con las fuentes reales; SIEM existente si el volumen y presupuesto lo justifican.
- **Mensajería:** comenzar con una cola gestionada o broker sencillo; añadir un bus distribuido solo cuando el volumen lo requiera.
- **Secretos:** una bóveda dedicada, identidades de workload y rotación automatizada; nunca secretos en variables de repositorio ni logs.
- **Interfaz SOC:** dashboard web con RBAC, cronología de incidentes, estado de agentes, evidencia y aprobaciones.
- **Despliegue:** entorno local reproducible y laboratorio aislado antes de producción; infraestructura declarativa y cambios revisables.

Antes de elegir productos concretos hay que conocer el entorno, el volumen de eventos, los activos, la disponibilidad exigida, el equipo operativo y el presupuesto. No se presupone que haya que comprar un rack ni desplegar un modelo de IA propio.

## 9. Alcance del MVP y fases

### Fase 0 — Requisitos y modelo de amenazas
- Inventariar activos, propietarios, flujos permitidos y límites de autorización.
- Identificar amenazas, impacto, dependencias y objetivos de recuperación.
- Definir qué acciones requieren aprobación y cómo se revierten.

### Fase 1 — Telemetría y auditoría
- Ingerir eventos de prueba con esquema versionado.
- Crear inventario mínimo de activos y fuentes.
- Persistir eventos, redactar datos sensibles y comprobar integridad.
- Construir una cronología básica de incidentes.

### Fase 2 — Detección sin acciones automáticas
- Implementar reglas deterministas iniciales y deduplicación.
- Mostrar severidad, confianza, evidencia y explicación.
- Medir falsos positivos y falsos negativos con datos sintéticos o autorizados.

### Fase 3 — Respuesta supervisada
- Crear solicitudes de acción, aprobaciones y auditoría.
- Empezar con acciones reversibles en un laboratorio.
- Probar expiración, idempotencia, rollback y fallos parciales.

### Fase 4 — Secretos y honeypots
- Integrar una bóveda en entorno de prueba.
- Desplegar honeypots aislados, sin rutas a producción y sin secretos reales.
- Verificar que la telemetría del señuelo llega al sistema sin abrir una vía de movimiento lateral.

### Fase 5 — Operación controlada
- Ensayar recuperación, rotación de credenciales, restauración y respuesta a incidentes.
- Establecer guardias, runbooks, métricas, retención y revisión periódica.
- Ampliar la automatización solo con evidencia de seguridad y aprobación operativa.

## 10. Pruebas de aceptación mínimas

- Una fuente no autenticada no puede inyectar eventos como si procedieran de un agente confiable.
- Un agente no puede ejecutar una acción fuera de su lista de permisos.
- Una acción crítica sin aprobación válida se rechaza y queda auditada.
- Repetir una solicitud no ejecuta dos veces una acción no idempotente.
- Una acción expirada o dirigida a un activo no inventariado se rechaza.
- La caída del servicio de IA no desactiva firewall, autenticación ni políticas de acceso.
- El registro permite detectar alteraciones en eventos o lotes firmados.
- Los datos sensibles se redactan y no aparecen en logs de aplicación.
- La honeynet no puede iniciar conexiones hacia producción ni acceder a secretos reales.
- Existe un procedimiento probado para revertir una contención y recuperar el servicio.

## 11. Riesgos y decisiones pendientes

| Riesgo / incógnita | Tratamiento necesario |
|---|---|
| Falsos positivos que interrumpan servicios | Umbrales medidos, acciones graduadas, expiración y revisión humana para alto impacto. |
| Agente o credencial comprometidos | Identidades separadas, permisos mínimos, límites de red y revocación independiente. |
| Manipulación o pérdida de logs | Copias protegidas, hashes firmados, monitorización de huecos y pruebas de restauración. |
| Honeynet usada como pivote | Aislamiento de red, salida bloqueada, datos ficticios y pruebas de contención. |
| Bloqueos que afecten a terceros legítimos | Preferir alcance estrecho, duración limitada y validación del contexto antes de bloquear. |
| IA alucinando o dando órdenes inseguras | IA solo propone; motor determinista valida y el ejecutor aplica allowlists. |
| Costes de infraestructura desconocidos | Dimensionar con métricas reales antes de adquirir hardware o licencias. |
| Privacidad y obligaciones legales | Definir finalidad, base jurídica, minimización, acceso y retención según jurisdicción. |

### Presupuesto

Las cifras de hardware, colocation, ancho de banda, anti-DDoS y SIEM del documento inicial son referencias orientativas, no ofertas verificadas ni una estimación aprobada. El coste real depende de tráfico, retención, proveedor, redundancia, SLA y personal. El MVP debe empezar en laboratorio con infraestructura existente o de bajo coste y presupuestar tras medir ingestión y almacenamiento.

## 12. Criterio de salida a producción

No desplegar respuesta autónoma en producción hasta que existan: inventario validado, modelo de amenazas, revisión de permisos, logs protegidos, pruebas de aceptación, runbooks de rollback, alertas de salud, aprobación de los responsables y un periodo de operación en modo observación. La autonomía es una capacidad que se gana con evidencia, no una configuración inicial.

---

## Historial de decisiones

- **D0 — Diseño inicial:** se adopta la separación por zonas, los seis roles de agentes y la regla de que la IA recomienda mientras la política determinista autoriza.
- **Pendiente:** stack definitivo, proveedores, esquema SQL físico, contratos OpenAPI, retención de datos, objetivos de disponibilidad y presupuesto validado.
