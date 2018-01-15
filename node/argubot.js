#! /usr/bin/env node



console.log("ARGUBOT");

const exec = require('child_process').exec;

var argubot_is_speaking = false;

const record = require('node-record-lpcm16');
const { Models, Detector } = require("snowboy");

const antonyms = {
  ja : 'nee',
  nee: 'ja',
  goed : 'fout',
  fout : 'goed',
  links : 'rechts',
  rechts : 'links',
  zwart : 'wit',
  wit : 'zwart'
}


const models = new Models();

for (key in antonyms) {
  models.add({
    file: '../models/snowboy/'+ key +'.pmdl',
    sensitivity: '0.5',
    hotwords : key
  });
}


const detector = new Detector({
  resource: "./node_modules/snowboy/resources/common.res",
  models: models,
  audioGain: 2.0
});

var cnt_silence = 0;
detector.on('silence', function () {
  if (++cnt_silence > 5) {
    console.log('ARGUBOT luistert...');
    cnt_silence = 0;
  }
});

detector.on('sound', function (buffer) {
  // <buffer> contains the last chunk of the audio that triggers the "sound"
  // event. It could be written to a wav stream.
  //console.log('sound');
});

detector.on('error', function () {
  console.log('error');
});

detector.on('hotword', function (index, hotword, buffer) {
  // <buffer> contains the last chunk of the audio that triggers the "hotword"
  // event. It could be written to a wav stream. You will have to use it
  // together with the <buffer> in the "sound" event if you want to get audio
  // data after the hotword.
  
   console.log(buffer);
  
  if (! argubot_is_speaking) {
    console.log('hotword detected', index, hotword);
    argubot_is_speaking = true;
    exec('espeak -vnl+m2 ' + antonyms[hotword] , function callback(error, stdout, stderr){
      setTimeout(function(){ 
        argubot_is_speaking = false; 
        console.log("finished",hotword);
      },250);
    });

  }
 
  

});

const mic = record.start({
  threshold: 0,
  verbose: false
});

mic.pipe(detector);

