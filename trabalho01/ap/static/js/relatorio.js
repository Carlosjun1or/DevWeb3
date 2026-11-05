const categorias = JSON.parse(document.getElementById('categorias').textContent);
    const quantidades = JSON.parse(document.getElementById('quantidades').textContent);
    const statusValores = JSON.parse(document.getElementById('status-valores').textContent);

    new Chart(document.getElementById('graficoCategorias'),{
        type: 'bar',
        data: {
            labels: categorias,
            datasets:[{
                label: 'Serviços por categoria',
                data: quantidades,
                backgroundColor: '#1e6b4f'
            }]

        }
    });

    new Chart(document.getElementById('graficoStatus'),{
        type:'doughnut',
        data: {
            labels: ['Ativos', 'Inativos'],
            datasets:[{
                label: 'Serviços por status',
                data: statusValores,
                backgroundColor: [
                    '#1e6b4f', 
                    '#2f956d'
                ]
            }]
        }
    });