namespace Freelance.Domain;

public sealed class TodoItem
{
    public Guid Id { get; init; }
    public string Title { get; init; } = string.Empty;
    public bool IsCompleted { get; private set; }

    public static TodoItem Create(string title)
    {
        if (string.IsNullOrWhiteSpace(title))
        {
            throw new ArgumentException("Title is required.", nameof(title));
        }

        return new TodoItem
        {
            Id = Guid.NewGuid(),
            Title = title.Trim(),
            IsCompleted = false
        };
    }
}

public interface ITodoRepository
{
    Task<IReadOnlyList<TodoItem>> GetAllAsync(CancellationToken cancellationToken = default);
    Task<TodoItem> AddAsync(TodoItem item, CancellationToken cancellationToken = default);
}
