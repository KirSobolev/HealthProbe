var socket = io.connect('http://' + document.domain + ':' + location.port);

        socket.on('connect', function () {
            console.log('Connected to server');
        });

        socket.on('update_humidity_plot', function (data) {
            updatePlot('humidity-plot-container', data.plot);
        });

        socket.on('update_temperature_plot', function (data) {
            updatePlot('temperature-plot-container', data.plot);
        });

        function updatePlot(containerId, plotData) {
            var plotImage = document.createElement('img');
            plotImage.src = 'data:image/png;base64,' + plotData;
            document.getElementById(containerId).innerHTML = '';
            document.getElementById(containerId).appendChild(plotImage);
        }