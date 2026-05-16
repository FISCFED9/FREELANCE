using Freelance.Domain;
using Microsoft.Extensions.DependencyInjection;

namespace Freelance.Application.DTOs
{
    public sealed record TodoItemDto(Guid Id, string Title, bool IsCompleted);
}

namespace Freelance.Application.Services
{
    using Freelance.Application.DTOs;

    public interface ITodoService
    {
        Task<IReadOnlyList<TodoItemDto>> GetAllAsync(CancellationToken cancellationToken = default);
        Task<TodoItemDto> CreateAsync(string title, CancellationToken cancellationToken = default);
    }

    internal sealed class GetTodoItemsUseCase
    {
        private readonly ITodoRepository repository;

        public GetTodoItemsUseCase(ITodoRepository repository)
        {
            this.repository = repository;
        }

        public async Task<IReadOnlyList<TodoItemDto>> ExecuteAsync(CancellationToken cancellationToken = default)
        {
            var items = await repository.GetAllAsync(cancellationToken);
            return items.Select(Map).ToArray();
        }

        private static TodoItemDto Map(TodoItem item) => new(item.Id, item.Title, item.IsCompleted);
    }

    internal sealed class CreateTodoItemUseCase
    {
        private readonly ITodoRepository repository;

        public CreateTodoItemUseCase(ITodoRepository repository)
        {
            this.repository = repository;
        }

        public async Task<TodoItemDto> ExecuteAsync(string title, CancellationToken cancellationToken = default)
        {
            var entity = TodoItem.Create(title);
            var stored = await repository.AddAsync(entity, cancellationToken);
            return new TodoItemDto(stored.Id, stored.Title, stored.IsCompleted);
        }
    }

    internal sealed class TodoService : ITodoService
    {
        private readonly GetTodoItemsUseCase getTodoItemsUseCase;
        private readonly CreateTodoItemUseCase createTodoItemUseCase;

        public TodoService(GetTodoItemsUseCase getTodoItemsUseCase, CreateTodoItemUseCase createTodoItemUseCase)
        {
            this.getTodoItemsUseCase = getTodoItemsUseCase;
            this.createTodoItemUseCase = createTodoItemUseCase;
        }

        public Task<IReadOnlyList<TodoItemDto>> GetAllAsync(CancellationToken cancellationToken = default)
            => getTodoItemsUseCase.ExecuteAsync(cancellationToken);

        public Task<TodoItemDto> CreateAsync(string title, CancellationToken cancellationToken = default)
            => createTodoItemUseCase.ExecuteAsync(title, cancellationToken);
    }
}

namespace Freelance.Application
{
    using Freelance.Application.Services;

    public static class DependencyInjection
    {
        public static IServiceCollection AddApplication(this IServiceCollection services)
        {
            services.AddScoped<GetTodoItemsUseCase>();
            services.AddScoped<CreateTodoItemUseCase>();
            services.AddScoped<ITodoService, TodoService>();
            return services;
        }
    }
}
