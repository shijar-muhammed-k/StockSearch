// Autocomplete Input Box

sortedList = phones.sort()
const phoneList = document.querySelector("#phoneList")
const inputbox = document.getElementById('phoneName')

function insertData(Plist, location, text){
    location.innerHTML = " "
    innerElement = " "
    for(element of Plist){
        boldLetter = '<b>' + element.substr(0, text.length) + '</b>'
        remaining = element.substr(text.length,element.length)
        word = boldLetter + remaining
        innerElement +=`<li onclick="listValue('${element}')">${word.toUpperCase()}</li>`;
    };
    location.innerHTML = innerElement
}

function filter(plist, text){
    // return plist.filter((x)=>x.toLowerCase().includes(text.toLowerCase()))
    wordList = []
    for(var x of plist) {
        if(x.toLowerCase().startsWith(text.toLowerCase())){
            wordList.push(x)
        }
    }
    return wordList
}

inputbox.addEventListener("input", function(){
    phoneList.style.display = 'block'
    data = filter(sortedList, inputbox.value)
    insertData(data, phoneList, inputbox.value)
})

function listValue(element){
    inputbox.value =  element.toUpperCase()
    phoneList.style.display = 'none'
    res(element)
}



function res(element){
    resBox = document.getElementById('resBox')
    if (phone[element].toLowerCase() == 'yes'){
        resBox.classList.remove('warning-msg')
        resBox.classList.add('success-msg')
    }
    else{
        resBox.classList.remove('success-msg')
        resBox.classList.add('warning-msg')
    }
    resBox.innerHTML = (phone[element]).toUpperCase()
}
