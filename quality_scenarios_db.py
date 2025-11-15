"""
Database of quality scenarios for ISO/IEC 25010 quality attributes.
This file serves as the single source of truth for all scenarios in both Spanish and English.
COMPLETED VERSION - All scenarios have options, correctOption, and explanation.
"""

import random

# Dictionary of quality scenarios with bilingual support
QUALITY_SCENARIOS_DB = [
    {
        "es": {
            "description": "Un sistema de gestión de inventario para una cadena de tiendas debe poder realizar actualizaciones de inventario en tiempo real sin retrasos perceptibles.",
            "category": "Eficiencia de desempeño",
            "options": {
                "A": "Eficiencia de desempeño",
                "B": "Fiabilidad",
                "C": "Usabilidad",
                "D": "Compatibilidad",
            },
            "correctOption": "A",
            "explanation": "Este escenario se relaciona con la Eficiencia de desempeño porque se enfoca en la velocidad de respuesta y el uso eficiente de recursos para realizar actualizaciones en tiempo real."
        },
        "en": {
            "description": "An inventory management system for a retail chain should be able to perform real-time inventory updates without perceptible delays.",
            "category": "Performance efficiency",
            "options": {
                "A": "Performance efficiency",
                "B": "Reliability",
                "C": "Usability",
                "D": "Compatibility",
            },
            "correctOption": "A",
            "explanation": "This scenario relates to Performance efficiency because it focuses on response speed and efficient use of resources to perform real-time updates."
        }
    },
    {
        "es": {
            "description": "Una aplicación bancaria debe garantizar que todas las transacciones financieras sean seguras y estén protegidas contra accesos no autorizados.",
            "category": "Seguridad",
            "options": {
                "A": "Usabilidad",
                "B": "Seguridad",
                "C": "Compatibilidad",
                "D": "Mantenibilidad",
            },
            "correctOption": "B",
            "explanation": "Este escenario se enfoca en la Seguridad ya que trata de proteger las transacciones financieras contra accesos no autorizados, lo cual es un aspecto clave de la seguridad de sistemas."
        },
        "en": {
            "description": "A banking application must ensure that all financial transactions are secure and protected against unauthorized access.",
            "category": "Security",
            "options": {
                "A": "Usability",
                "B": "Security",
                "C": "Compatibility",
                "D": "Maintainability",
            },
            "correctOption": "B",
            "explanation": "This scenario focuses on Security as it deals with protecting financial transactions against unauthorized access, which is a key aspect of system security."
        }
    },
    {
        "es": {
            "description": "Un sistema de gestión de aprendizaje debe ser fácil de usar para profesores sin experiencia técnica, permitiéndoles crear cursos sin formación adicional.",
            "category": "Usabilidad",
            "options": {
                "A": "Compatibilidad",
                "B": "Fiabilidad",
                "C": "Usabilidad",
                "D": "Portabilidad",
            },
            "correctOption": "C",
            "explanation": "Este escenario se centra en la Usabilidad ya que habla específicamente de que el sistema sea fácil de usar para usuarios sin experiencia técnica, lo cual es un aspecto fundamental de la usabilidad."
        },
        "en": {
            "description": "A learning management system should be easy to use for teachers without technical experience, allowing them to create courses without additional training.",
            "category": "Usability",
            "options": {
                "A": "Compatibility",
                "B": "Reliability",
                "C": "Usability",
                "D": "Portability",
            },
            "correctOption": "C",
            "explanation": "This scenario centers on Usability as it specifically talks about the system being easy to use for users without technical experience, which is a fundamental aspect of usability."
        }
    },
    {
        "es": {
            "description": "Un software de gestión de proyectos debe poder integrarse con herramientas de correo electrónico y calendario para sincronizar automáticamente tareas y reuniones.",
            "category": "Compatibilidad",
            "options": {
                "A": "Seguridad",
                "B": "Mantenibilidad",
                "C": "Compatibilidad",
                "D": "Eficiencia de desempeño",
            },
            "correctOption": "C",
            "explanation": "Este escenario se refiere a la Compatibilidad porque trata sobre la capacidad del software para integrarse con otros sistemas (correo electrónico y calendario), lo que es un aspecto clave de la compatibilidad."
        },
        "en": {
            "description": "Project management software should be able to integrate with email and calendar tools to automatically synchronize tasks and meetings.",
            "category": "Compatibility",
            "options": {
                "A": "Security",
                "B": "Maintainability",
                "C": "Compatibility",
                "D": "Performance efficiency",
            },
            "correctOption": "C",
            "explanation": "This scenario refers to Compatibility because it deals with the software's ability to integrate with other systems (email and calendar), which is a key aspect of compatibility."
        }
    },
    {
        "es": {
            "description": "Una aplicación de comercio electrónico debe tener un tiempo de recuperación menor a 5 minutos después de una falla del sistema para minimizar la pérdida de ventas.",
            "category": "Fiabilidad",
            "options": {
                "A": "Eficiencia de desempeño",
                "B": "Fiabilidad",
                "C": "Seguridad",
                "D": "Usabilidad",
            },
            "correctOption": "B",
            "explanation": "Este escenario está relacionado con la Fiabilidad porque trata sobre el tiempo de recuperación después de una falla, lo cual es un aspecto clave de la fiabilidad y disponibilidad del sistema."
        },
        "en": {
            "description": "An e-commerce application should have a recovery time of less than 5 minutes after a system failure to minimize sales loss.",
            "category": "Reliability",
            "options": {
                "A": "Performance efficiency",
                "B": "Reliability",
                "C": "Security",
                "D": "Usability",
            },
            "correctOption": "B",
            "explanation": "This scenario is related to Reliability because it deals with recovery time after a failure, which is a key aspect of system reliability and availability."
        }
    },
    {
        "es": {
            "description": "Un sistema de historias clínicas electrónicas debe mantener la consistencia de los datos del paciente incluso cuando múltiples médicos actualicen el registro simultáneamente.",
            "category": "Fiabilidad",
            "options": {
                "A": "Compatibilidad",
                "B": "Mantenibilidad",
                "C": "Fiabilidad",
                "D": "Seguridad",
            },
            "correctOption": "C",
            "explanation": "Este escenario corresponde a Fiabilidad porque se refiere a la capacidad del sistema para mantener la consistencia de los datos en condiciones de uso concurrente, lo cual es un aspecto de la fiabilidad de los sistemas."
        },
        "en": {
            "description": "An electronic health record system must maintain consistency of patient data even when multiple doctors update the record simultaneously.",
            "category": "Reliability",
            "options": {
                "A": "Compatibility",
                "B": "Maintainability",
                "C": "Reliability",
                "D": "Security",
            },
            "correctOption": "C",
            "explanation": "This scenario corresponds to Reliability because it refers to the system's ability to maintain data consistency under concurrent use conditions, which is an aspect of system reliability."
        }
    },
    {
        "es": {
            "description": "Un software de análisis de datos debe ser capaz de procesar conjuntos de datos de 1 TB en menos de una hora para permitir decisiones comerciales oportunas.",
            "category": "Eficiencia de desempeño",
            "options": {
                "A": "Eficiencia de desempeño",
                "B": "Usabilidad",
                "C": "Portabilidad",
                "D": "Compatibilidad",
            },
            "correctOption": "A",
            "explanation": "Este escenario está relacionado con la Eficiencia de desempeño ya que se centra en la capacidad del software para procesar grandes volúmenes de datos en un tiempo específico, lo que es un aspecto fundamental del rendimiento del sistema."
        },
        "en": {
            "description": "Data analysis software should be able to process 1 TB datasets in less than one hour to enable timely business decisions.",
            "category": "Performance efficiency",
            "options": {
                "A": "Performance efficiency",
                "B": "Usability",
                "C": "Portability",
                "D": "Compatibility",
            },
            "correctOption": "A",
            "explanation": "This scenario is related to Performance efficiency as it focuses on the software's ability to process large volumes of data in a specific timeframe, which is a fundamental aspect of system performance."
        }
    },
    {
        "es": {
            "description": "Un sistema de autenticación debe proteger contra ataques de fuerza bruta limitando los intentos de inicio de sesión y utilizando verificación de dos factores.",
            "category": "Seguridad",
            "options": {
                "A": "Fiabilidad",
                "B": "Compatibilidad",
                "C": "Seguridad",
                "D": "Usabilidad",
            },
            "correctOption": "C",
            "explanation": "Este escenario se centra en la Seguridad porque aborda la protección contra ataques y el uso de métodos de verificación para garantizar que solo usuarios autorizados accedan al sistema."
        },
        "en": {
            "description": "An authentication system should protect against brute force attacks by limiting login attempts and using two-factor verification.",
            "category": "Security",
            "options": {
                "A": "Reliability",
                "B": "Compatibility",
                "C": "Security",
                "D": "Usability",
            },
            "correctOption": "C",
            "explanation": "This scenario focuses on Security because it addresses protection against attacks and the use of verification methods to ensure only authorized users access the system."
        }
    },
    {
        "es": {
            "description": "Un sistema de gestión de contenidos debe permitir a los editores modificar la estructura del sitio web sin requerir conocimientos de programación.",
            "category": "Usabilidad",
            "options": {
                "A": "Mantenibilidad",
                "B": "Usabilidad",
                "C": "Portabilidad",
                "D": "Compatibilidad",
            },
            "correctOption": "B",
            "explanation": "Este escenario corresponde a Usabilidad porque se enfoca en hacer el sistema accesible y fácil de usar para personas sin conocimientos técnicos específicos."
        },
        "en": {
            "description": "A content management system should allow editors to modify website structure without requiring programming knowledge.",
            "category": "Usability",
            "options": {
                "A": "Maintainability",
                "B": "Usability",
                "C": "Portability",
                "D": "Compatibility",
            },
            "correctOption": "B",
            "explanation": "This scenario corresponds to Usability because it focuses on making the system accessible and easy to use for people without specific technical knowledge."
        }
    },
    {
        "es": {
            "description": "Una aplicación móvil debe funcionar correctamente en diferentes versiones de sistemas operativos, desde Android 8 hasta la versión más reciente.",
            "category": "Portabilidad",
            "options": {
                "A": "Compatibilidad",
                "B": "Fiabilidad",
                "C": "Portabilidad",
                "D": "Mantenibilidad",
            },
            "correctOption": "C",
            "explanation": "Este escenario está relacionado con la Portabilidad porque trata de la capacidad del software para ejecutarse en diferentes entornos (distintas versiones del sistema operativo)."
        },
        "en": {
            "description": "A mobile application should function correctly on different operating system versions, from Android 8 to the most recent version.",
            "category": "Portability",
            "options": {
                "A": "Compatibility",
                "B": "Reliability",
                "C": "Portability",
                "D": "Maintainability",
            },
            "correctOption": "C",
            "explanation": "This scenario is related to Portability because it deals with the software's ability to run in different environments (different operating system versions)."
        }
    },
    {
        "es": {
            "description": "Un sistema de control de tráfico debe tener un tiempo medio entre fallos (MTBF) de al menos 10,000 horas para garantizar la seguridad vial.",
            "category": "Fiabilidad",
            "options": {
                "A": "Eficiencia de desempeño",
                "B": "Fiabilidad",
                "C": "Seguridad",
                "D": "Mantenibilidad",
            },
            "correctOption": "B",
            "explanation": "Este escenario se relaciona con la Fiabilidad porque se enfoca en el tiempo medio entre fallos (MTBF), que es una medida directa de la capacidad del sistema para mantener su funcionamiento sin fallos durante un período específico."
        },
        "en": {
            "description": "A traffic control system should have a mean time between failures (MTBF) of at least 10,000 hours to ensure road safety.",
            "category": "Reliability",
            "options": {
                "A": "Performance efficiency",
                "B": "Reliability",
                "C": "Security",
                "D": "Maintainability",
            },
            "correctOption": "B",
            "explanation": "This scenario relates to Reliability because it focuses on mean time between failures (MTBF), which is a direct measure of the system's ability to maintain its operation without failures for a specific period."
        }
    },
    {
        "es": {
            "description": "Un software de edición de video debe utilizar eficientemente los recursos del sistema para evitar que la computadora se ralentice durante el procesamiento de videos de alta resolución.",
            "category": "Eficiencia de desempeño",
            "options": {
                "A": "Eficiencia de desempeño",
                "B": "Usabilidad",
                "C": "Fiabilidad",
                "D": "Portabilidad",
            },
            "correctOption": "A",
            "explanation": "Este escenario se relaciona con la Eficiencia de desempeño porque se enfoca en el uso eficiente de los recursos del sistema (CPU, memoria, etc.) para mantener un rendimiento óptimo durante tareas intensivas."
        },
        "en": {
            "description": "Video editing software should efficiently use system resources to prevent the computer from slowing down while processing high-resolution videos.",
            "category": "Performance efficiency",
            "options": {
                "A": "Performance efficiency",
                "B": "Usability",
                "C": "Reliability",
                "D": "Portability",
            },
            "correctOption": "A",
            "explanation": "This scenario relates to Performance efficiency because it focuses on the efficient use of system resources (CPU, memory, etc.) to maintain optimal performance during intensive tasks."
        }
    },
    {
        "es": {
            "description": "Una plataforma de pagos online debe cifrar la información de la tarjeta de crédito utilizando estándares actualizados para prevenir el robo de datos.",
            "category": "Seguridad",
            "options": {
                "A": "Compatibilidad",
                "B": "Seguridad",
                "C": "Fiabilidad",
                "D": "Usabilidad",
            },
            "correctOption": "B",
            "explanation": "Este escenario se relaciona con la Seguridad porque se enfoca en la protección de datos sensibles (información de tarjetas de crédito) mediante cifrado para prevenir accesos no autorizados."
        },
        "en": {
            "description": "An online payment platform should encrypt credit card information using up-to-date standards to prevent data theft.",
            "category": "Security",
            "options": {
                "A": "Compatibility",
                "B": "Security",
                "C": "Reliability",
                "D": "Usability",
            },
            "correctOption": "B",
            "explanation": "This scenario relates to Security because it focuses on protecting sensitive data (credit card information) through encryption to prevent unauthorized access."
        }
    },
    {
        "es": {
            "description": "Un software de diseño arquitectónico debe proporcionar retroalimentación visual inmediata cuando los usuarios modifiquen elementos de diseño para una experiencia intuitiva.",
            "category": "Usabilidad",
            "options": {
                "A": "Usabilidad",
                "B": "Eficiencia de desempeño",
                "C": "Portabilidad",
                "D": "Mantenibilidad",
            },
            "correctOption": "A",
            "explanation": "Este escenario se relaciona con la Usabilidad porque se enfoca en proporcionar retroalimentación inmediata e intuitiva para mejorar la experiencia del usuario durante la interacción con el software."
        },
        "en": {
            "description": "Architectural design software should provide immediate visual feedback when users modify design elements for an intuitive experience.",
            "category": "Usability",
            "options": {
                "A": "Usability",
                "B": "Performance efficiency",
                "C": "Portability",
                "D": "Maintainability",
            },
            "correctOption": "A",
            "explanation": "This scenario relates to Usability because it focuses on providing immediate and intuitive feedback to improve user experience during software interaction."
        }
    },
    {
        "es": {
            "description": "Un sistema de automatización industrial debe poder comunicarse con equipos de diferentes fabricantes utilizando protocolos estándar.",
            "category": "Compatibilidad",
            "options": {
                "A": "Compatibilidad",
                "B": "Portabilidad",
                "C": "Mantenibilidad",
                "D": "Seguridad",
            },
            "correctOption": "A",
            "explanation": "Este escenario se relaciona con la Compatibilidad porque se enfoca en la capacidad del sistema para interactuar y comunicarse con equipos de diferentes fabricantes mediante protocolos estándar."
        },
        "en": {
            "description": "An industrial automation system should be able to communicate with equipment from different manufacturers using standard protocols.",
            "category": "Compatibility",
            "options": {
                "A": "Compatibility",
                "B": "Portability",
                "C": "Maintainability",
                "D": "Security",
            },
            "correctOption": "A",
            "explanation": "This scenario relates to Compatibility because it focuses on the system's ability to interact and communicate with equipment from different manufacturers through standard protocols."
        }
    },
    {
        "es": {
            "description": "Una aplicación de videoconferencia debe mantener la sincronización de audio y video incluso con conexiones a internet inestables.",
            "category": "Fiabilidad",
            "options": {
                "A": "Eficiencia de desempeño",
                "B": "Fiabilidad",
                "C": "Usabilidad",
                "D": "Compatibilidad",
            },
            "correctOption": "B",
            "explanation": "Este escenario se relaciona con la Fiabilidad porque se enfoca en mantener la funcionalidad (sincronización) del sistema bajo condiciones adversas (conexiones inestables)."
        },
        "en": {
            "description": "A videoconferencing application should maintain audio and video synchronization even with unstable internet connections.",
            "category": "Reliability",
            "options": {
                "A": "Performance efficiency",
                "B": "Reliability",
                "C": "Usability",
                "D": "Compatibility",
            },
            "correctOption": "B",
            "explanation": "This scenario relates to Reliability because it focuses on maintaining system functionality (synchronization) under adverse conditions (unstable connections)."
        }
    },
    {
        "es": {
            "description": "Un software de renderizado 3D debe aprovechar la aceleración por hardware para maximizar la velocidad de generación de imágenes complejas.",
            "category": "Eficiencia de desempeño",
            "options": {
                "A": "Eficiencia de desempeño",
                "B": "Portabilidad",
                "C": "Mantenibilidad",
                "D": "Usabilidad",
            },
            "correctOption": "A",
            "explanation": "Este escenario se relaciona con la Eficiencia de desempeño porque se enfoca en maximizar la velocidad de procesamiento mediante el uso óptimo de recursos de hardware."
        },
        "en": {
            "description": "3D rendering software should leverage hardware acceleration to maximize the speed of generating complex images.",
            "category": "Performance efficiency",
            "options": {
                "A": "Performance efficiency",
                "B": "Portability",
                "C": "Maintainability",
                "D": "Usability",
            },
            "correctOption": "A",
            "explanation": "This scenario relates to Performance efficiency because it focuses on maximizing processing speed through optimal use of hardware resources."
        }
    },
    {
        "es": {
            "description": "Un sistema de votación electrónica debe implementar medidas para prevenir la manipulación de votos y garantizar la integridad del proceso electoral.",
            "category": "Seguridad",
            "options": {
                "A": "Compatibilidad",
                "B": "Seguridad",
                "C": "Fiabilidad",
                "D": "Usabilidad",
            },
            "correctOption": "B",
            "explanation": "Este escenario se relaciona con la Seguridad porque se enfoca en la protección de información y datos contra accesos no autorizados."
        },
        "en": {
            "description": "3D rendering software should leverage hardware acceleration to maximize the speed of generating complex images.",
            "category": "Performance efficiency",
            "options": {
                "A": "Performance efficiency",
                "B": "Usability",
                "C": "Reliability",
                "D": "Portability",
            },
            "correctOption": "A",
            "explanation": "This scenario relates to Performance efficiency because it focuses on optimal use of system resources to maximize performance."
        }
    },
    {
        "es": {
            "description": "Un sistema de votación electrónica debe implementar medidas para prevenir la manipulación de votos y garantizar la integridad del proceso electoral.",
            "category": "Seguridad",
            "options": {
                "A": "Compatibilidad",
                "B": "Seguridad",
                "C": "Fiabilidad",
                "D": "Usabilidad",
            },
            "correctOption": "B",
            "explanation": "Este escenario se relaciona con la Seguridad porque se enfoca en la protección de información y datos contra accesos no autorizados."
        },
        "en": {
            "description": "An electronic voting system should implement measures to prevent vote tampering and ensure the integrity of the electoral process.",
            "category": "Security",
            "options": {
                "A": "Compatibility",
                "B": "Security",
                "C": "Reliability",
                "D": "Usability",
            },
            "correctOption": "B",
            "explanation": "This scenario relates to Security because it focuses on protecting information and data against unauthorized access."
        }
    },
    {
        "es": {
            "description": "Una aplicación de navegación debe proporcionar instrucciones claras y oportunas para ayudar a los conductores a tomar decisiones rápidas en el tráfico.",
            "category": "Usabilidad",
            "options": {
                "A": "Usabilidad",
                "B": "Eficiencia de desempeño",
                "C": "Portabilidad",
                "D": "Mantenibilidad",
            },
            "correctOption": "A",
            "explanation": "Este escenario se relaciona con la Usabilidad porque se enfoca en la facilidad de uso y la experiencia del usuario al interactuar con el sistema."
        },
        "en": {
            "description": "A navigation application should provide clear and timely instructions to help drivers make quick decisions in traffic.",
            "category": "Usability",
            "options": {
                "A": "Usability",
                "B": "Performance efficiency",
                "C": "Portability",
                "D": "Maintainability",
            },
            "correctOption": "A",
            "explanation": "This scenario relates to Usability because it focuses on ease of use and user experience when interacting with the system."
        }
    },
    {
        "es": {
            "description": "Un software de gestión empresarial debe poder exportar datos en formatos compatibles con herramientas de análisis como Excel y Power BI.",
            "category": "Compatibilidad",
            "options": {
                "A": "Compatibilidad",
                "B": "Portabilidad",
                "C": "Mantenibilidad",
                "D": "Seguridad",
            },
            "correctOption": "A",
            "explanation": "Este escenario se relaciona con la Compatibilidad porque se enfoca en la capacidad del sistema para coexistir e intercambiar información con otros sistemas."
        },
        "en": {
            "description": "Business management software should be able to export data in formats compatible with analysis tools such as Excel and Power BI.",
            "category": "Compatibility",
            "options": {
                "A": "Compatibility",
                "B": "Portability",
                "C": "Maintainability",
                "D": "Security",
            },
            "correctOption": "A",
            "explanation": "This scenario relates to Compatibility because it focuses on the system's ability to coexist and exchange information with other systems."
        }
    },
    {
        "es": {
            "description": "Una plataforma de streaming debe mantener la calidad del servicio incluso durante picos de tráfico en eventos importantes.",
            "category": "Fiabilidad",
            "options": {
                "A": "Eficiencia de desempeño",
                "B": "Fiabilidad",
                "C": "Seguridad",
                "D": "Mantenibilidad",
            },
            "correctOption": "B",
            "explanation": "Este escenario se relaciona con la Fiabilidad porque se enfoca en la capacidad del sistema para mantener su funcionamiento bajo condiciones específicas durante un período determinado."
        },
        "en": {
            "description": "A streaming platform should maintain service quality even during traffic spikes during important events.",
            "category": "Reliability",
            "options": {
                "A": "Performance efficiency",
                "B": "Reliability",
                "C": "Security",
                "D": "Maintainability",
            },
            "correctOption": "B",
            "explanation": "This scenario relates to Reliability because it focuses on the system's ability to maintain its operation under specified conditions for a specified period."
        }
    },
    {
        "es": {
            "description": "Un sistema de reserva de vuelos debe procesar transacciones simultáneas de miles de usuarios sin degradación del rendimiento durante ventas especiales.",
            "category": "Eficiencia de desempeño",
            "options": {
                "A": "Eficiencia de desempeño",
                "B": "Usabilidad",
                "C": "Fiabilidad",
                "D": "Portabilidad",
            },
            "correctOption": "A",
            "explanation": "Este escenario se relaciona con la Eficiencia de desempeño porque se enfoca en el uso óptimo de recursos del sistema para maximizar el rendimiento."
        },
        "en": {
            "description": "A flight booking system should process simultaneous transactions from thousands of users without performance degradation during special sales.",
            "category": "Performance efficiency",
            "options": {
                "A": "Performance efficiency",
                "B": "Usability",
                "C": "Reliability",
                "D": "Portability",
            },
            "correctOption": "A",
            "explanation": "This scenario relates to Performance efficiency because it focuses on optimal use of system resources to maximize performance."
        }
    },
    {
        "es": {
            "description": "Una aplicación de banca móvil debe implementar verificación biométrica para autorizar transacciones sensibles y proteger la información financiera del usuario.",
            "category": "Seguridad",
            "options": {
                "A": "Compatibilidad",
                "B": "Seguridad",
                "C": "Fiabilidad",
                "D": "Usabilidad",
            },
            "correctOption": "B",
            "explanation": "Este escenario se relaciona con la Seguridad porque se enfoca en la protección de información y datos contra accesos no autorizados."
        },
        "en": {
            "description": "A mobile banking application should implement biometric verification to authorize sensitive transactions and protect user financial information.",
            "category": "Security",
            "options": {
                "A": "Compatibility",
                "B": "Security",
                "C": "Reliability",
                "D": "Usability",
            },
            "correctOption": "B",
            "explanation": "This scenario relates to Security because it focuses on protecting information and data against unauthorized access."
        }
    },
    {
        "es": {
            "description": "Un software de gestión de tareas debe ofrecer opciones de personalización que permitan a los usuarios adaptar la interfaz según sus preferencias y flujos de trabajo.",
            "category": "Usabilidad",
            "options": {
                "A": "Usabilidad",
                "B": "Eficiencia de desempeño",
                "C": "Portabilidad",
                "D": "Mantenibilidad",
            },
            "correctOption": "A",
            "explanation": "Este escenario se relaciona con la Usabilidad porque se enfoca en la facilidad de uso y la experiencia del usuario al interactuar con el sistema."
        },
        "en": {
            "description": "Task management software should offer customization options that allow users to adapt the interface according to their preferences and workflows.",
            "category": "Usability",
            "options": {
                "A": "Usability",
                "B": "Performance efficiency",
                "C": "Portability",
                "D": "Maintainability",
            },
            "correctOption": "A",
            "explanation": "This scenario relates to Usability because it focuses on ease of use and user experience when interacting with the system."
        }
    },
    {
        "es": {
            "description": "Un sistema de almacenamiento en la nube debe ser compatible con diferentes dispositivos y sistemas operativos para permitir el acceso a los archivos desde cualquier plataforma.",
            "category": "Compatibilidad",
            "options": {
                "A": "Compatibilidad",
                "B": "Portabilidad",
                "C": "Mantenibilidad",
                "D": "Seguridad",
            },
            "correctOption": "A",
            "explanation": "Este escenario se relaciona con la Compatibilidad porque se enfoca en la capacidad del sistema para coexistir e intercambiar información con otros sistemas."
        },
        "en": {
            "description": "A cloud storage system should be compatible with different devices and operating systems to allow file access from any platform.",
            "category": "Compatibility",
            "options": {
                "A": "Compatibility",
                "B": "Portability",
                "C": "Maintainability",
                "D": "Security",
            },
            "correctOption": "A",
            "explanation": "This scenario relates to Compatibility because it focuses on the system's ability to coexist and exchange information with other systems."
        }
    },
    {
        "es": {
            "description": "Un software médico debe realizar copias de seguridad automáticas de la información crítica del paciente para evitar pérdidas de datos en caso de fallos del sistema.",
            "category": "Fiabilidad",
            "options": {
                "A": "Eficiencia de desempeño",
                "B": "Fiabilidad",
                "C": "Seguridad",
                "D": "Mantenibilidad",
            },
            "correctOption": "B",
            "explanation": "Este escenario se relaciona con la Fiabilidad porque se enfoca en la capacidad del sistema para mantener su funcionamiento bajo condiciones específicas durante un período determinado."
        },
        "en": {
            "description": "Medical software should perform automatic backups of critical patient information to prevent data loss in case of system failures.",
            "category": "Reliability",
            "options": {
                "A": "Performance efficiency",
                "B": "Reliability",
                "C": "Security",
                "D": "Maintainability",
            },
            "correctOption": "B",
            "explanation": "This scenario relates to Reliability because it focuses on the system's ability to maintain its operation under specified conditions for a specified period."
        }
    },
    {
        "es": {
            "description": "Un motor de búsqueda debe devolver resultados relevantes en menos de 500 milisegundos para proporcionar una experiencia de usuario fluida.",
            "category": "Eficiencia de desempeño",
            "options": {
                "A": "Eficiencia de desempeño",
                "B": "Usabilidad",
                "C": "Fiabilidad",
                "D": "Portabilidad",
            },
            "correctOption": "A",
            "explanation": "Este escenario se relaciona con la Eficiencia de desempeño porque se enfoca en el uso óptimo de recursos del sistema para maximizar el rendimiento."
        },
        "en": {
            "description": "A search engine should return relevant results in less than 500 milliseconds to provide a smooth user experience.",
            "category": "Performance efficiency",
            "options": {
                "A": "Performance efficiency",
                "B": "Usability",
                "C": "Reliability",
                "D": "Portability",
            },
            "correctOption": "A",
            "explanation": "This scenario relates to Performance efficiency because it focuses on optimal use of system resources to maximize performance."
        }
    },
    {
        "es": {
            "description": "Un sistema de gestión de identidades debe implementar protección contra el robo de sesiones mediante tokens de seguridad y tiempos de expiración adecuados.",
            "category": "Seguridad",
            "options": {
                "A": "Compatibilidad",
                "B": "Seguridad",
                "C": "Fiabilidad",
                "D": "Usabilidad",
            },
            "correctOption": "B",
            "explanation": "Este escenario se relaciona con la Seguridad porque se enfoca en la protección de información y datos contra accesos no autorizados."
        },
        "en": {
            "description": "An identity management system should implement protection against session hijacking using security tokens and appropriate expiration times.",
            "category": "Security",
            "options": {
                "A": "Compatibility",
                "B": "Security",
                "C": "Reliability",
                "D": "Usability",
            },
            "correctOption": "B",
            "explanation": "This scenario relates to Security because it focuses on protecting information and data against unauthorized access."
        }
    },
    {
        "es": {
            "description": "Una aplicación de edición de fotografías debe ofrecer una interfaz intuitiva con herramientas claramente etiquetadas y accesibles para usuarios novatos.",
            "category": "Usabilidad",
            "options": {
                "A": "Usabilidad",
                "B": "Eficiencia de desempeño",
                "C": "Portabilidad",
                "D": "Mantenibilidad",
            },
            "correctOption": "A",
            "explanation": "Este escenario se relaciona con la Usabilidad porque se enfoca en la facilidad de uso y la experiencia del usuario al interactuar con el sistema."
        },
        "en": {
            "description": "A photo editing application should offer an intuitive interface with clearly labeled and accessible tools for novice users.",
            "category": "Usability",
            "options": {
                "A": "Usability",
                "B": "Performance efficiency",
                "C": "Portability",
                "D": "Maintainability",
            },
            "correctOption": "A",
            "explanation": "This scenario relates to Usability because it focuses on ease of use and user experience when interacting with the system."
        }
    },
    {
        "es": {
            "description": "Un software de colaboración debe funcionar correctamente con diferentes navegadores web y sus distintas versiones para garantizar la accesibilidad universal.",
            "category": "Portabilidad",
            "options": {
                "A": "Compatibilidad",
                "B": "Fiabilidad",
                "C": "Portabilidad",
                "D": "Mantenibilidad",
            },
            "correctOption": "C",
            "explanation": "Este escenario se relaciona con la Portabilidad porque se enfoca en la capacidad del sistema para ser transferido de un entorno a otro."
        },
        "en": {
            "description": "Collaboration software should function correctly with different web browsers and their various versions to ensure universal accessibility.",
            "category": "Portability",
            "options": {
                "A": "Compatibility",
                "B": "Reliability",
                "C": "Portability",
                "D": "Maintainability",
            },
            "correctOption": "C",
            "explanation": "This scenario relates to Portability because it focuses on the system's ability to be transferred from one environment to another."
        }
    }
]

def get_random_scenarios(num_scenarios=5, quality_attribute=None, language="es", force_new_selection=False):
    """
    Return random scenarios from database. All scenarios are now complete.
    """
    import random
    
    # Use system time for randomness
    random.seed()
    
    print(f"🎲 Getting {num_scenarios} random scenarios in {language}")
    
    # Get scenarios with requested language - all should be complete now
    available = [s for s in QUALITY_SCENARIOS_DB if language in s]
    print(f"📊 Using {len(available)} scenarios")
    
    # Select randomly
    if len(available) >= num_scenarios:
        selected = random.sample(available, num_scenarios)
    else:
        selected = available
    
    # Convert to expected format
    result = []
    for scenario in selected:
        data = scenario[language]
        result.append({
            "id": str(random.randint(1000, 9999)),
            "content": data["description"],
            "options": data["options"],
            "correctOption": data["correctOption"],
            "explanation": data["explanation"],
            "category": data.get("category", "General")
        })
    
    print(f"✅ Returning {len(result)} scenarios")
    return result

def get_database_stats():
    """Return statistics about the database."""
    # Count scenarios by quality attribute
    by_attribute = {}
    attributes = set()
    
    for scenario in QUALITY_SCENARIOS_DB:
        if "es" in scenario:
            category = scenario["es"].get("category", "Unknown")
            attributes.add(category)
            if category in by_attribute:
                by_attribute[category] += 1
            else:
                by_attribute[category] = 1
    
    return {
        "total_scenarios": len(QUALITY_SCENARIOS_DB),
        "languages": ["es", "en"],
        "complete": True,
        "attributes": list(attributes),
        "by_attribute": by_attribute
    }
