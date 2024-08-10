document.addEventListener('DOMContentLoaded', fetchData);

async function fetchData() {
  const response = await fetch('/api/data'); 
  const data = await response.json();

  const container = document.getElementById('data-container');


  data.forEach(item => {
    const div = document.createElement('div');
    div.classList.add('notify-item');

    const timestamp = new Date(item.timestamp).toLocaleString();
    const sensorValue = item.sensor_value;
    const problem = item.problem;
    const iconLink = item.icon_link;

    div.innerHTML = `
      <div class="notify_img">
        <img src="${iconLink}" alt="Icon" class="icon">
      </div>
      <div class="notify_info">
        <p>${problem}</p>
        <p>${sensorValue}</p>
        <span class="notify_time">${timestamp}</span>
      </div>`;

    container.appendChild(div);
  });
}
