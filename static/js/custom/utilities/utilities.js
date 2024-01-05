/**
 * Show an element by changing its CSS classes.
 * @param {string} idElementHtml - ID of the element to be shown.
 * @param {Function[]} showFunctions - An array of functions to execute when showing the element.
 */
function showElement({ idElementHtml, functions = [] }){
    const element = document.getElementById(idElementHtml);

    if (element) {
        element.classList.add('d-block')
        element.classList.remove('d-none')
        executeFunctions(functions)
    }

}

/**
 * Hide an element by changing its CSS classes.
 * @param {string} idElementHtml - ID of the element to be hidden.
 */
function hideElement({ idElementHtml, functions = [] }) {
    const element = document.getElementById(idElementHtml);

    if (element) {
        element.classList.add('d-none')
        element.classList.remove('d-block')
        executeFunctions(functions)
    }
}

/**
 * Formatea el título del elemento con el ID proporcionado.
 * Capitaliza la primera letra y convierte el resto a minúsculas.
 * @param {string} idInputElement - ID del elemento input.
 */
function formatAndSetTitle(inputElement) {
    // Obtener el valor del elemento, eliminar espacios en blanco al principio y al final
    const inputValue = inputElement.value;

    // Formatear el texto: capitalizar la primera letra, convertir el resto a minúsculas
    const formattedText = inputValue.charAt(0).toUpperCase() + inputValue.slice(1).toLowerCase();
    // Establecer el título del elemento formateado
    inputElement.value = formattedText;
}

/**
 * Executes an array of functions.
 *
 * @param {Function[]} functions - An array of functions to be executed.
 */
function executeFunctions(functions) {
    for (const func of functions) {
        func();
    }
}

/**
 * Get the text of the selected option in a select element.
 * @param {string} idSelectElement - ID of the select element.
 * @returns {string} Text of the selected option.
 */
function getSelectedText(idSelectElement) {
    const selectedHtml = document.getElementById(idSelectElement);
    const selectedValue = selectedHtml.options[selectedHtml.selectedIndex].text
    return selectedValue
}

export { showElement, hideElement, formatAndSetTitle, executeFunctions, getSelectedText }