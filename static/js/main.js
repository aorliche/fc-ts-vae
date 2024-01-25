const $ = q => document.querySelector(q);
const $$ = q => [...document.querySelectorAll(q)];

window.addEventListener('load', () => {
    $('#number').addEventListener('input', () => {
        let val = $('#number').value;
        val = 10 ** parseFloat(val);
        $('#number-value').innerText = Math.round(val);
    });
    $('#age').addEventListener('input', () => {
        let val = $('#age').value;
        $('#age-value').innerText = parseInt(val);
    });
    $('#preset').addEventListener('change', () => {
        const idx = $('#preset').selectedIndex;
        const val = $('#preset').options[idx].value;
        let [age, sex, race, task] = val.split('-');
        age = parseInt(age);
        $('#age').value = age;
        $('#age-value').innerText = age;
        if (sex == 'male') {
            $('#male').checked = true;
        } else {
            $('#female').checked = true;
        }
        for (let i=0; i<$('#race').options.length; i++) {
            if ($('#race').options[i].value == race) {
                $('#race').selectedIndex = i;
                break;
            }
        }
        for (let i=0; i<$('#task').options.length; i++) {
            if ($('#task').options[i].value == task) {
                $('#task').selectedIndex = i;
                break;
            }
        }
    });
    let nscans = 0;
    function scanUpdater() {
        nscans++;
        $('#scan1').max = nscans-1;
        $('#scan2').max = nscans-1;
    }
    $('#generate').addEventListener('click', scanUpdater);
    $('#generate-var').addEventListener('click', scanUpdater);
});
