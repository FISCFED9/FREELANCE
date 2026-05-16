using Freelance.Application;
using Freelance.Application.Services;
using Freelance.Infrastructure;
using Microsoft.Extensions.DependencyInjection;

namespace Freelance.Api.Tests;

public class TaskFlowTests
{
    [Fact]
    public async Task CreateAndListTask_StoresItemInRepository()
    {
        var services = new ServiceCollection();
        services.AddApplication();
        services.AddInfrastructure();

        using var provider = services.BuildServiceProvider();
        var service = provider.GetRequiredService<ITodoService>();

        var created = await service.CreateAsync("Preparar propuesta");
        var items = await service.GetAllAsync();

        Assert.NotEqual(Guid.Empty, created.Id);
        Assert.Contains(items, x => x.Id == created.Id && x.Title == "Preparar propuesta");
    }
}