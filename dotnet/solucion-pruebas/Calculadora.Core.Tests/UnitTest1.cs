using Calculadora.Core;

namespace Calculadora.Core.Tests;

public class OperacionesTests
{
    [Fact]
    public void Sumar_DosNumeros_RetornaSuma()
    {
        var resultado = Operaciones.Sumar(2, 3);
        Assert.Equal(5, resultado);
    }

    [Fact]
    public void Restar_DosNumeros_RetornaResta()
    {
        var resultado = Operaciones.Restar(7, 4);
        Assert.Equal(3, resultado);
    }
}
