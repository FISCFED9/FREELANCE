# Plantilla Base .NET para FREELANCE

Plantilla con Clean Architecture para APIs en .NET 8.

## Estructura

- src/Freelance.Api: capa de entrada (endpoints HTTP).
- src/Freelance.Application: casos de uso y orquestacion.
- src/Freelance.Domain: entidades y contratos del negocio.
- src/Freelance.Infrastructure: implementaciones tecnicas (repositorios).
- tests/Freelance.Api.Tests: pruebas de integracion livianas.

## Flujo actual de ejemplo

- POST /api/tasks crea una tarea.
- GET /api/tasks lista tareas.

## Comandos

- dotnet restore FreelanceTemplate.sln
- dotnet build FreelanceTemplate.sln
- dotnet test FreelanceTemplate.sln
