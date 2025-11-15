#!/usr/bin/env python
"""
Script to update requirements_scenarios.json to bilingual format
"""

import json

# Complete bilingual scenarios data
bilingual_scenarios = {
  "game_info": {
    "name": "RequirementRally",
    "version": "1.0.0",
    "description": {
      "en": "Educational game to practice identifying requirement types",
      "es": "Juego educativo para practicar la identificación de tipos de requisitos"
    },
    "total_scenarios": 20,
    "categories": ["Functional", "Non-Functional", "Constraint"],
    "languages": ["en", "es"]
  },
  "scenarios": [
    {
      "id": "req_001",
      "content": {
        "en": "The system must allow registered users to log in using their email and password.",
        "es": "El sistema debe permitir que los usuarios registrados puedan iniciar sesión utilizando su email y contraseña."
      },
      "options": {
        "en": ["Functional", "Non-Functional", "Constraint", "Not a requirement"],
        "es": ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
      },
      "correctOption": "A",
      "explanation": {
        "en": "This is a functional requirement because it describes a specific function that the system must perform: authenticate users through credentials.",
        "es": "Es un requisito funcional porque describe una función específica que el sistema debe realizar: autenticar usuarios mediante credenciales."
      },
      "category": "Functional",
      "difficulty": "easy"
    },
    {
      "id": "req_002",
      "content": {
        "en": "The system must respond to search queries in less than 2 seconds.",
        "es": "El sistema debe responder a las consultas de búsqueda en menos de 2 segundos."
      },
      "options": {
        "en": ["Functional", "Non-Functional", "Constraint", "Not a requirement"],
        "es": ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
      },
      "correctOption": "B",
      "explanation": {
        "en": "This is a non-functional requirement because it specifies a performance criterion (response time) that the system must meet.",
        "es": "Es un requisito no-funcional porque especifica un criterio de rendimiento (tiempo de respuesta) que el sistema debe cumplir."
      },
      "category": "Non-Functional",
      "difficulty": "easy"
    },
    {
      "id": "req_003",
      "content": {
        "en": "Development must be done using only open-source technologies.",
        "es": "El desarrollo debe realizarse utilizando únicamente tecnologías de código abierto."
      },
      "options": {
        "en": ["Functional", "Non-Functional", "Constraint", "Not a requirement"],
        "es": ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
      },
      "correctOption": "C",
      "explanation": {
        "en": "This is a constraint because it limits the technological options available for development, without specifying functionality.",
        "es": "Es una restricción porque limita las opciones tecnológicas disponibles para el desarrollo, sin especificar funcionalidad."
      },
      "category": "Constraint",
      "difficulty": "medium"
    },
    {
      "id": "req_004",
      "content": {
        "en": "The system must generate monthly sales reports in PDF format.",
        "es": "El sistema debe generar reportes de ventas mensuales en formato PDF."
      },
      "options": {
        "en": ["Functional", "Non-Functional", "Constraint", "Not a requirement"],
        "es": ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
      },
      "correctOption": "A",
      "explanation": {
        "en": "This is a functional requirement because it describes a specific system capability: generating reports in a determined format.",
        "es": "Es un requisito funcional porque describe una capacidad específica del sistema: generar reportes en un formato determinado."
      },
      "category": "Functional",
      "difficulty": "easy"
    },
    {
      "id": "req_005",
      "content": {
        "en": "The system must be available 99.9% of the time during business hours.",
        "es": "El sistema debe estar disponible 99.9% del tiempo durante horarios laborales."
      },
      "options": {
        "en": ["Functional", "Non-Functional", "Constraint", "Not a requirement"],
        "es": ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
      },
      "correctOption": "B",
      "explanation": {
        "en": "This is a non-functional availability requirement that specifies a service level the system must maintain.",
        "es": "Es un requisito no-funcional de disponibilidad, especifica un nivel de servicio que debe mantener el sistema."
      },
      "category": "Non-Functional",
      "difficulty": "easy"
    },
    {
      "id": "req_006",
      "content": {
        "en": "The project budget must not exceed $50,000 USD.",
        "es": "El presupuesto del proyecto no debe exceder los $50,000 USD."
      },
      "options": {
        "en": ["Functional", "Non-Functional", "Constraint", "Not a requirement"],
        "es": ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
      },
      "correctOption": "C",
      "explanation": {
        "en": "This is a project constraint that limits the available financial resources, it doesn't describe system functionality.",
        "es": "Es una restricción del proyecto que limita los recursos financieros disponibles, no describe funcionalidad del sistema."
      },
      "category": "Constraint",
      "difficulty": "medium"
    },
    {
      "id": "req_007",
      "content": {
        "en": "Users must be able to filter products by category, price, and brand.",
        "es": "Los usuarios deben poder filtrar productos por categoría, precio y marca."
      },
      "options": {
        "en": ["Functional", "Non-Functional", "Constraint", "Not a requirement"],
        "es": ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
      },
      "correctOption": "A",
      "explanation": {
        "en": "This is a functional requirement because it describes specific filtering functions that the system must provide to users.",
        "es": "Es un requisito funcional porque describe funciones específicas de filtrado que el sistema debe proporcionar a los usuarios."
      },
      "category": "Functional",
      "difficulty": "easy"
    },
    {
      "id": "req_008",
      "content": {
        "en": "The interface must be intuitive and easy to use for users without technical experience.",
        "es": "La interfaz debe ser intuitiva y fácil de usar para usuarios sin experiencia técnica."
      },
      "options": {
        "en": ["Functional", "Non-Functional", "Constraint", "Not a requirement"],
        "es": ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
      },
      "correctOption": "B",
      "explanation": {
        "en": "This is a non-functional usability requirement that specifies qualitative characteristics of the user experience.",
        "es": "Es un requisito no-funcional de usabilidad, especifica características cualitativas de la experiencia del usuario."
      },
      "category": "Non-Functional",
      "difficulty": "medium"
    },
    {
      "id": "req_009",
      "content": {
        "en": "The system must be developed following the company's coding standards.",
        "es": "El sistema debe desarrollarse siguiendo los estándares de codificación de la empresa."
      },
      "options": {
        "en": ["Functional", "Non-Functional", "Constraint", "Not a requirement"],
        "es": ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
      },
      "correctOption": "C",
      "explanation": {
        "en": "This is a constraint that establishes rules about how the software should be developed, not what it should do.",
        "es": "Es una restricción que establece reglas sobre cómo debe desarrollarse el software, no qué debe hacer."
      },
      "category": "Constraint",
      "difficulty": "medium"
    },
    {
      "id": "req_010",
      "content": {
        "en": "The system must send email notifications when a transaction is completed.",
        "es": "El sistema debe enviar notificaciones por email cuando se complete una transacción."
      },
      "options": {
        "en": ["Functional", "Non-Functional", "Constraint", "Not a requirement"],
        "es": ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
      },
      "correctOption": "A",
      "explanation": {
        "en": "This is a functional requirement because it describes a specific action that the system must perform: sending notifications.",
        "es": "Es un requisito funcional porque describe una acción específica que el sistema debe realizar: enviar notificaciones."
      },
      "category": "Functional",
      "difficulty": "easy"
    },
    {
      "id": "req_011",
      "content": {
        "en": "The system must support up to 1000 concurrent users without performance degradation.",
        "es": "El sistema debe soportar hasta 1000 usuarios concurrentes sin degradación del rendimiento."
      },
      "options": {
        "en": ["Functional", "Non-Functional", "Constraint", "Not a requirement"],
        "es": ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
      },
      "correctOption": "B",
      "explanation": {
        "en": "This is a non-functional scalability requirement that specifies system capacity limits.",
        "es": "Es un requisito no-funcional de escalabilidad que especifica límites de capacidad del sistema."
      },
      "category": "Non-Functional",
      "difficulty": "medium"
    },
    {
      "id": "req_012",
      "content": {
        "en": "The development team must deliver a beta version in 3 months.",
        "es": "El equipo de desarrollo debe entregar una versión beta en 3 meses."
      },
      "options": {
        "en": ["Functional", "Non-Functional", "Constraint", "Not a requirement"],
        "es": ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
      },
      "correctOption": "C",
      "explanation": {
        "en": "This is a temporal project constraint that establishes delivery deadlines, not system functionality.",
        "es": "Es una restricción temporal del proyecto que establece plazos de entrega, no funcionalidad del sistema."
      },
      "category": "Constraint",
      "difficulty": "medium"
    },
    {
      "id": "req_013",
      "content": {
        "en": "Personal data must be encrypted both in transit and at rest.",
        "es": "Los datos personales deben estar encriptados tanto en tránsito como en reposo."
      },
      "options": {
        "en": ["Functional", "Non-Functional", "Constraint", "Not a requirement"],
        "es": ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
      },
      "correctOption": "B",
      "explanation": {
        "en": "This is a non-functional security requirement that specifies how data should be protected.",
        "es": "Es un requisito no-funcional de seguridad que especifica cómo deben protegerse los datos."
      },
      "category": "Non-Functional",
      "difficulty": "medium"
    },
    {
      "id": "req_014",
      "content": {
        "en": "The system must allow exporting data in CSV and Excel formats.",
        "es": "El sistema debe permitir exportar datos en formatos CSV y Excel."
      },
      "options": {
        "en": ["Functional", "Non-Functional", "Constraint", "Not a requirement"],
        "es": ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
      },
      "correctOption": "A",
      "explanation": {
        "en": "This is a functional requirement because it describes a specific system capability: exporting data in determined formats.",
        "es": "Es un requisito funcional porque describe una capacidad específica del sistema: exportar datos en formatos determinados."
      },
      "category": "Functional",
      "difficulty": "easy"
    },
    {
      "id": "req_015",
      "content": {
        "en": "The application must be compatible with Chrome, Firefox, and Safari browsers.",
        "es": "La aplicación debe ser compatible con navegadores Chrome, Firefox y Safari."
      },
      "options": {
        "en": ["Functional", "Non-Functional", "Constraint", "Not a requirement"],
        "es": ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
      },
      "correctOption": "B",
      "explanation": {
        "en": "This is a non-functional compatibility requirement that specifies which environments the system must work in.",
        "es": "Es un requisito no-funcional de compatibilidad que especifica en qué entornos debe funcionar el sistema."
      },
      "category": "Non-Functional",
      "difficulty": "medium"
    },
    {
      "id": "req_016",
      "content": {
        "en": "Only authorized personnel can access the production server.",
        "es": "Solo el personal autorizado puede acceder al servidor de producción."
      },
      "options": {
        "en": ["Functional", "Non-Functional", "Constraint", "Not a requirement"],
        "es": ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
      },
      "correctOption": "C",
      "explanation": {
        "en": "This is an organizational security constraint that limits access, not a system functionality.",
        "es": "Es una restricción de seguridad organizacional que limita el acceso, no una funcionalidad del sistema."
      },
      "category": "Constraint",
      "difficulty": "hard"
    },
    {
      "id": "req_017",
      "content": {
        "en": "Users must be able to reset their password through a link sent by email.",
        "es": "Los usuarios deben poder restablecer su contraseña mediante un enlace enviado por email."
      },
      "options": {
        "en": ["Functional", "Non-Functional", "Constraint", "Not a requirement"],
        "es": ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
      },
      "correctOption": "A",
      "explanation": {
        "en": "This is a functional requirement because it describes a specific process that the system must implement for password recovery.",
        "es": "Es un requisito funcional porque describe un proceso específico que el sistema debe implementar para la recuperación de contraseñas."
      },
      "category": "Functional",
      "difficulty": "medium"
    },
    {
      "id": "req_018",
      "content": {
        "en": "Planned downtime for maintenance must not exceed 4 hours monthly.",
        "es": "El tiempo de inactividad planificado para mantenimiento no debe exceder 4 horas mensuales."
      },
      "options": {
        "en": ["Functional", "Non-Functional", "Constraint", "Not a requirement"],
        "es": ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
      },
      "correctOption": "B",
      "explanation": {
        "en": "This is a non-functional availability requirement that establishes limits for system maintenance.",
        "es": "Es un requisito no-funcional de disponibilidad que establece límites para el mantenimiento del sistema."
      },
      "category": "Non-Functional",
      "difficulty": "hard"
    },
    {
      "id": "req_019",
      "content": {
        "en": "Source code must be versioned using Git and hosted in private repositories.",
        "es": "El código fuente debe estar versionado usando Git y alojado en repositorios privados."
      },
      "options": {
        "en": ["Functional", "Non-Functional", "Constraint", "Not a requirement"],
        "es": ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
      },
      "correctOption": "C",
      "explanation": {
        "en": "This is a constraint that establishes specific tools and processes for development, not system functionality.",
        "es": "Es una restricción que establece herramientas y procesos específicos para el desarrollo, no funcionalidad del sistema."
      },
      "category": "Constraint",
      "difficulty": "hard"
    },
    {
      "id": "req_020",
      "content": {
        "en": "The system must maintain a complete log of all transactions for auditing purposes.",
        "es": "El sistema debe mantener un registro completo de todas las transacciones para auditoría."
      },
      "options": {
        "en": ["Functional", "Non-Functional", "Constraint", "Not a requirement"],
        "es": ["Funcional", "No-Funcional", "Restricción", "No es un requisito"]
      },
      "correctOption": "A",
      "explanation": {
        "en": "This is a functional requirement because it describes a specific system capability: recording and maintaining transaction logs.",
        "es": "Es un requisito funcional porque describe una capacidad específica del sistema: registrar y mantener logs de transacciones."
      },
      "category": "Functional",
      "difficulty": "medium"
    }
  ]
}

# Write the updated JSON file
with open('requirements_scenarios.json', 'w', encoding='utf-8') as f:
    json.dump(bilingual_scenarios, f, indent=2, ensure_ascii=False)

print("✅ Updated requirements_scenarios.json to bilingual format")
print("📊 Total scenarios: 20")
print("🌐 Languages: English, Spanish")
print("📝 Categories: Functional, Non-Functional, Constraint")