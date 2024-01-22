async function apiGetRequest(apiEndPoint, idElementValue) {
    try {
        // Manually build the API URL
        //const value = document.getElementById(idElementValue).value
        let baseUrl = apiEndPoint.replace('EXAMPLE', '');
        let value = idElementValue



        const apiUrl = `${baseUrl}${value}`;
        const response = await fetch(apiUrl);

        console.log(apiUrl)
        // Throw an error if the response is not successful
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        // Get the JSON object from the response
        const wordInfo = await response.json();

        // Check if each wordType has id and value properties
        wordInfo.forEach(wordType => {
            
        });

    } catch (error) {
        console.error('Error:', error.message);
    }
}


export { apiGetRequest }
