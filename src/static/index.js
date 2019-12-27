document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#form').onsubmit = () => {

        const request = new XMLHttpRequest();
        const postcode = document.querySelector('#postcode-input').value;

        request.open('POST', '/postcode');

        request.onload = () => {
            const data = JSON.parse(request.responseText);

            if (data.success) {
                const result = data.result;
                let content = `<div>Postcode: ${result.postcode}</div>`;
                content += `<div>${result.admin_district}, ${result.region}, ${result.country} </div>`;
                document.querySelector('#result').innerHTML = content;
            }
            else {
                document.querySelector('#result').innerHTML = 'There was an error.';
            }
        };

        const data = new FormData();
        data.append('postcode', postcode);
        request.send(data);

        return false;
    };

});
