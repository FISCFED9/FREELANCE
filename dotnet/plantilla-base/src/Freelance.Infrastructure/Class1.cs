using Freelance.Domain;
using Microsoft.Extensions.DependencyInjection;

namespace Freelance.Infrastructure;

internal sealed class InMemoryTodoRepository : ITodoRepository
{
    private readonly List<TodoItem> items = new();

    public Task<IReadOnlyList<TodoItem>> GetAllAsync(CancellationToken cancellationToken = default)
    {
        IReadOnlyList<TodoItem> snapshot = items
            .OrderBy(x => x.Title)
            .ToArray();
        return Task.FromResult(snapshot);
    }

    public Task<TodoItem> AddAsync(TodoItem item, CancellationToken cancellationToken = default)
    {
        items.Add(item);
        return Task.FromResult(item);
    }
}

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(this IServiceCollection services)
    {
        services.AddSingleton<ITodoRepository, InMemoryTodoRepository>();
        return services;
    }
}
