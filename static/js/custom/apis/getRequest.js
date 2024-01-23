async function apiGetRequest(apiEndPoint, idElementValue) {
    try {
        // Manually build the API URL
        //const value = document.getElementById(idElementValue).value
        let baseUrl = apiEndPoint.replace('EXAMPLE', '');
        let value = idElementValue



        let apiUrl = `${baseUrl}${value}`;
        let response = await fetch(apiUrl);

        console.log(apiUrl)
        // Throw an error if the response is not successful
        console.log(response.ok)
        if (!response.ok) {
            return null;
        }

        // Get the JSON object from the response
        let wordInfo = await response.json();
        return wordInfo;  

    } catch (error) {
        console.error('Error:', error.message);
        return null;
    }
}


export { apiGetRequest }
