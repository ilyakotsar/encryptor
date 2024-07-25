async function post(url, data) {
	const options = {
		method: 'POST',
		credentials: 'same-origin',
		headers: {'Content-Type': 'application/json'},
		referrerPolicy: 'no-referrer',
		body: JSON.stringify(data),
	};
	const response = await fetch(url, options);
	return response.json();
}

function symmetric_encrypt() {
	const data = {
		encrypt: true,
		plaintext: document.getElementById('plaintext').value,
		time_cost: document.getElementById('time_cost').value,
		memory_cost: document.getElementById('memory_cost').value,
		parallelism: document.getElementById('parallelism').value,
		password: document.getElementById('password').value,
	}
	post('/symmetric', data).then(res => {
		document.getElementById('encrypted_message').value = res['encrypted_message'];
	});
}

function symmetric_decrypt() {
	const data = {
		decrypt: true,
		encrypted_message: document.getElementById('encrypted_message').value,
		password: document.getElementById('password').value,
	}
	post('/symmetric', data).then(res => {
		document.getElementById('plaintext').value = res['plaintext'];
		document.getElementById('time_cost').value = res['time_cost'];
		document.getElementById('memory_cost').value = res['memory_cost'];
		document.getElementById('parallelism').value = res['parallelism'];
		document.getElementById('time_cost_display').textContent = res['time_cost'];
		document.getElementById('memory_cost_display').textContent = res['memory_cost'];
		document.getElementById('parallelism_display').textContent = res['parallelism'];
	});
}

function copy(btn, id) {
	navigator.clipboard.writeText(document.getElementById(id).value).then(() => {
		btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="m10 15.586-3.293-3.293-1.414 1.414L10 18.414l9.707-9.707-1.414-1.414z"></path></svg>';
		setTimeout(() => {
			btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M20 2H10c-1.103 0-2 .897-2 2v4H4c-1.103 0-2 .897-2 2v10c0 1.103.897 2 2 2h10c1.103 0 2-.897 2-2v-4h4c1.103 0 2-.897 2-2V4c0-1.103-.897-2-2-2zM4 20V10h10l.002 10H4zm16-6h-4v-4c0-1.103-.897-2-2-2h-4V4h10v10z"></path></svg>';
		}, '1000');
	});
}

function setValue(input) {
	document.getElementById(`${input.id}_display`).textContent = input.value;
}