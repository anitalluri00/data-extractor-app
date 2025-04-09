function upload() {
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];
  if (!file) return alert("Please select a file");

  const formData = new FormData();
  formData.append('file', file);

  fetch('http://localhost:5000/upload', {
    method: 'POST',
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    const output = document.getElementById('output');
    output.innerHTML = '';

    if (data.type === 'txt') {
      output.innerHTML = `<pre>${data.content}</pre>`;
    } else if (data.type === 'table') {
      const table = document.createElement('table');
      const thead = document.createElement('thead');
      const headerRow = document.createElement('tr');
      data.columns.forEach(col => {
        const th = document.createElement('th');
        th.innerText = col;
        headerRow.appendChild(th);
      });
      thead.appendChild(headerRow);
      table.appendChild(thead);

      const tbody = document.createElement('tbody');
      data.rows.forEach(row => {
        const tr = document.createElement('tr');
        data.columns.forEach(col => {
          const td = document.createElement('td');
          td.innerText = row[col];
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });
      table.appendChild(tbody);
      output.appendChild(table);
    } else {
      output.innerText = "Unknown file type or error occurred.";
    }
  })
  .catch(err => {
    console.error(err);
    alert("Error uploading file.");
  });
}
