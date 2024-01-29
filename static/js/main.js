const $ = q => document.querySelector(q);
const $$ = q => [...document.querySelectorAll(q)];

const pnc = {
    atlas: ['Power264'],
    age_mu: 14.6,
    age_sigma: 3.4,
    age_min: 8,
    age_max: 22,
    diag: null,
    task: [['rest', 'nback', 'emoid'], ['Resting State', 'Working Memory (nback)', 'Emotion Recognition (emoid)']], 
};

const bsnip = {
    atlas: ['Power264'],
    age_mu: 36.9,
    age_sigma: 12.3,
    age_min: 15,
    age_max: 64,
    diag: [['nc', 'sz'], ['Control', 'Schizophrenia']],
    task: null,
};

window.addEventListener('load', () => {
    $('#dataset').addEventListener('change', () => {
        const dataset = $('#dataset').value;
        let ds;
        switch (dataset) {
            case 'pnc': ds = pnc; break;
            case 'bsnip': ds = bsnip; break;
        }
        if (!ds) return;
        $('#age_mu').value = ds.age_mu;
        $('#age_sigma').value = ds.age_sigma;
        $('#age').min = ds.age_min;
        $('#age').max = ds.age_max;
        $('#age-value').innerText = parseInt($('#age').value);
        if (ds.diag == null) {
            $('#diag-div').style.display = 'none';
        } else {
            $('#diag-div').style.display = 'block';
            $('#diag').innerHTML = '';
            for (let i=0; i<ds.diag[0].length; i++) {
                const opt = document.createElement('option');
                opt.value = ds.diag[0][i];
                opt.innerText = ds.diag[1][i];
                $('#diag').appendChild(opt);
            }
        }
        if (ds.task == null) {
            $('#task-div').style.display = 'none';
        } else {
            $('#task-div').style.display = 'block';
            $('#task').innerHTML = '';
            for (let i=0; i<ds.task[0].length; i++) {
                const opt = document.createElement('option');
                opt.value = ds.task[0][i];
                opt.innerText = ds.task[1][i];
                $('#task').appendChild(opt);
            }
        }
    });
    $('#number').addEventListener('input', () => {
        let val = $('#number').value;
        val = 10 ** parseFloat(val);
        $('#number-value').innerText = Math.round(val);
    });
    $('#age').addEventListener('input', () => {
        let val = $('#age').value;
        $('#age-value').innerText = parseInt(val);
    });
    /*$('#preset').addEventListener('change', () => {
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
    });*/
    let nscans = 0;
    function scanUpdater() {
        nscans++;
        $('#scan1').max = nscans-1;
        $('#scan2').max = nscans-1;
    }
    $('#generate').addEventListener('click', scanUpdater);
    $('#generate-var').addEventListener('click', scanUpdater);
});
