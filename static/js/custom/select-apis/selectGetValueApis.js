
import { showElement, hideElement, getSelectedText } from '../utilities/utilities.js';

/**
 * Get options from an API endpoint and add them to a select element.
 * @param {string} idApiEndPointElement - ID of the element containing the API endpoint data attribute.
 * @param {string} idSelectElement - ID of the select element to which options will be added.
 * @param {string} dataEndPoint - Name of the data attribute containing the URL of the API endpoint.
 * @throws {Error} If the API response is not successful or if the wordType object lacks id and value properties.
 */
async function getOptionElements(idApiEndPointElement, idSelectElement, dataEndPoint) {
    try {
        // Manually build the API URL
        const apiEndpoint = document.getElementById(idApiEndPointElement).getAttribute(dataEndPoint)
        const response = await fetch(apiEndpoint);

        // Throw an error if the response is not successful
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        // Get the JSON object from the response
        const wordTypes = await response.json();

        // Check if each wordType has id and value properties
        wordTypes.forEach(wordType => {
            if (!wordType.id || !wordType.value) {
                throw new Error('Cada objeto wordType debe tener las propiedades id y value.');
            }
        });

        // Get the select element
        const selectElement = document.getElementById(idSelectElement);

        // Add an option for each word type
        wordTypes.forEach(wordType => {
            const option = document.createElement('option');
            if (selectElement.tagName.toLowerCase() === 'select') {
                option.value = wordType.id;
            }
            option.text = wordType.value;
            selectElement.appendChild(option);
        });

        // Here you can handle the response, for example, update the DOM with the data
    } catch (error) {
        console.error('Error:', error.message);
    }
}



/**
 * Show or hide an HTML element based on the selected value in another select element.
 * @param {string} value - Value to compare with the selection of the select element.
 * @param {string} idSelectElement - ID of the select element.
 * @param {string} idElementHtml - ID of the element to be shown or hidden.
 * @param {Function[]} showFunctions - An array of functions to execute when showing the element.
 * @param {Function[]} hideFunctions - An array of functions to execute when hiding the element.
 */
function showHideSelectElementByValue({value, idSelectElement, idElementHtml, showFunctions = [], hideFunctions= []}){
    const selectedValue = getSelectedText(idSelectElement)

    if (selectedValue === value) {
        showElement(
            {
                idElementHtml: idElementHtml,
                functions: showFunctions
            }
        )
    }else{
        hideElement(
            {
                idElementHtml: idElementHtml,
                functions: hideFunctions
            }
        )
    }
}

export { getOptionElements, showHideSelectElementByValue }
