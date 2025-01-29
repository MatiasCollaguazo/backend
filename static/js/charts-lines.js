/**
 * For usage, visit Chart.js docs https://www.chartjs.org/docs/latest/
 */


const lineConfig = {
  type: 'line',
  data: {
    labels: [], // Inicialmente vacío
    datasets: [
      {
        label: 'Respuestas por día',
        backgroundColor: '#0694a2',
        borderColor: '#0694a2',
        data: [], // Inicialmente vacío
        fill: false,
      },
    ],
  },
  options: {
    responsive: true,
    legend: {
      display: false,
    },
    tooltips: {
      mode: 'index',
      intersect: false,
    },
    hover: {
      mode: 'nearest',
      intersect: true,
    },
    scales: {
      x: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Día',
        },
      },
      y: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Respuestas',
        },
        beginAtZero: true,
      },
    },
  },
};

const countResponsesPerDay = (data) => {
  const counts = {}; // Objeto para almacenar los conteos por día
  const labels = []; // Array para almacenar los días únicos

  // Recorrer cada respuesta en el JSON
  Object.values(data).forEach(response => {
    const savedTime = response.saved;

    // Verificar si savedTime está definido
    if (!savedTime) {
      console.error('Fecha no definida en:', response);
      return;
    }

    // Parsear la fecha y hora manualmente
    const [datePart, timePart, ampm] = savedTime.match(/(\d{2}\/\d{2}\/\d{4}), (\d{2}:\d{2}:\d{2}) ([ap]\. m\.)/).slice(1);

    // Convertir la hora a formato 24 horas
    let [hours, minutes, seconds] = timePart.split(':').map(Number);
    if (ampm === 'p. m.' && hours !== 12) {
      hours += 12;
    } else if (ampm === 'a. m.' && hours === 12) {
      hours = 0;
    }

    // Convertir la fecha a formato Date
    const [day, month, year] = datePart.split('/').map(Number);
    const date = new Date(year, month - 1, day, hours, minutes, seconds);

    // Verificar si la fecha es válida
    if (isNaN(date.getTime())) {
      console.error('Fecha inválida:', savedTime);
      return;
    }

    // Formatear la fecha como "DD/MM/YYYY"
    const formattedDate = date.toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });

    // Si el día no está en el objeto counts, inicializarlo en 0
    if (!counts[formattedDate]) {
      counts[formattedDate] = 0;
      labels.push(formattedDate); // Agregar el día a las etiquetas
    }

    // Incrementar el conteo para ese día
    counts[formattedDate]++;
  });

  // Ordenar los días de forma ascendente
  labels.sort((a, b) => {
    const dateA = new Date(a.split('/').reverse().join('-'));
    const dateB = new Date(b.split('/').reverse().join('-'));
    return dateA - dateB;
  });

  // Devolver un objeto con las etiquetas y los conteos
  return {
    labels: labels,
    counts: labels.map(label => counts[label])
  };
};


// Inicializar la gráfica
const lineCtx = document.getElementById('line');
window.myLine = new Chart(lineCtx, lineConfig);

// Actualizar la gráfica cada 60 segundos (opcional)

const update = () => {
  fetch('/api/v1/landing') // Hacer una solicitud a la API
    .then(response => response.json()) // Convertir la respuesta a JSON
    .then(data => {
      // Procesar los datos para obtener las etiquetas y los conteos
      const { labels, counts } = countResponsesPerDay(data);

      // Actualizar los datos de la gráfica
      window.myLine.data.labels = labels;
      window.myLine.data.datasets[0].data = counts;

      // Actualizar la gráfica
      window.myLine.update();
    })
    .catch(error => console.error('Error:', error)); // Manejar errores
};

update();
