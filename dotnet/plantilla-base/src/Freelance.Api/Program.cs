using Freelance.Application;
using Freelance.Application.DTOs;
using Freelance.Application.Services;
using Freelance.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddApplication();
builder.Services.AddInfrastructure();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

var tasks = app.MapGroup("/api/tasks").WithTags("Tasks");

tasks.MapGet("/", async (ITodoService service, CancellationToken ct) =>
{
    var items = await service.GetAllAsync(ct);
    return Results.Ok(items);
})
.WithName("GetTasks")
.WithOpenApi();

tasks.MapPost("/", async (CreateTaskRequest request, ITodoService service, CancellationToken ct) =>
{
    var item = await service.CreateAsync(request.Title, ct);
    return Results.Created($"/api/tasks/{item.Id}", item);
})
.WithName("CreateTask")
.WithOpenApi();

app.Run();

public sealed record CreateTaskRequest(string Title);
