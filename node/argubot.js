#! /usr/bin/env node



console.log("argubot");

const exec = require('child_process').exec;

var stopListening = false;

const record = require('node-record-lpcm16');
const { Models, Detector } = require("snowboy");

const models = new Models();

models.add({
  file: './node_modules/snowboy/resources/snowboy.umdl',
  sensitivity: '0.5',
  hotwords : 'snowboy'
});

const detector = new Detector({
  resource: "./node_modules/snowboy/resources/common.res",
  models: models,
  audioGain: 2.0
});

detector.on('silence', function () {
  console.log('silence');
});

detector.on('sound', function (buffer) {
  // <buffer> contains the last chunk of the audio that triggers the "sound"
  // event. It could be written to a wav stream.
  console.log('sound');
});

detector.on('error', function () {
  console.log('error');
});

detector.on('hotword', function (index, hotword, buffer) {
  // <buffer> contains the last chunk of the audio that triggers the "hotword"
  // event. It could be written to a wav stream. You will have to use it
  // together with the <buffer> in the "sound" event if you want to get audio
  // data after the hotword.
  
  // console.log(buffer);


  console.log('hotword', index, hotword);
  if (! stopListening) {
    stopListening = true;
    exec('espeak -vnl+f3 "ach margrietje de rozen zullen bloeien, ook al zie je mij niet meer"', function callback(error, stdout, stderr){
      console.log("finished");
      stopListening = false;
    });
  }
 
  

});

const mic = record.start({
  threshold: 0,
  verbose: true
});

mic.pipe(detector);
