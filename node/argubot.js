#! /usr/bin/env node

const exec = require('child_process').exec;
const blessed = require('blessed');
const contrib = require('blessed-contrib');
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


const screen = blessed.screen({
  smartCSR: true
});

const cons = contrib.log({ 
  border: {
    type: 'line'
  },
  label: 'CONSOLE',
  width: '80%',
  height: '15%',
  top: '70%',
  left: 'center'
});

const wave = contrib.line({ 
  label: 'AUDIO',
  border: {
    type: 'line'
  },
  top: '10%',
  width: '80%',
  height: '60%',
  left: 'center',
  numYLabels: 5,
  style:{ 
     line: [255,255,0],
     text: [0,255,0],
     baseline: [0,0,0]
  }
})

const create_bt = function(message) { 
    return blessed.bigtext({
    content: ' ' + message + ' ',
    border: { type: 'line' },
    padding: { top: 1, bottom: 1, left: 0, right:  2},
    width: 'shrink',
    left: "center",
    top: "center",
    height: 20,
    style: {  
      bg: '#ff0000',
      fg: '#ffffff', 
      border: { fg: '#ffffff', bg: '#ff0000'}
      }
    });
  }

screen.append(wave); 
screen.append(cons);


const arr_x = [...Array(100).keys()];
const arr_y = arr_x.map(function(value, i){ return 127 + 127*Math.sin(value);});

wave.setData([ {
  x: arr_x,
  y: arr_y
}])


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

var argubot_is_speaking = false;
var cnt_silence = 0;
var dots='';
detector.on('silence', function () {
  if (++cnt_silence > 3 && ! argubot_is_speaking) {
    cons.log(' ARGUBOT luistert' + dots);
    dots = (dots.length < 5)? dots+"." : "";
    cnt_silence = 0;
  }
});

detector.on('sound', function (buffer) {
  const ratio  = Math.floor(buffer.length/100);
  const arr = buffer.filter(function (value, index, ar) {
      return (index % ratio == 0);
  } );

  wave.setData([ {
     x: arr.map(function(v,i){ return i}),
     y: arr
  }])
});

detector.on('error', function () {
  cons.log(' error');
});

detector.on('hotword', function (index, hotword, buffer) {
  if (! argubot_is_speaking) {
    cons.log(' U zegt ' + hotword);
    argubot_is_speaking = true;
    var bt = create_bt(antonyms[hotword]);
    screen.append(bt);
    setTimeout(function(){ 
        bt.destroy();
      },100);
    exec('espeak -vnl+m2 ' + antonyms[hotword] , function callback(error, stdout, stderr){
      setTimeout(function(){ 
        argubot_is_speaking = false; 
      },250);
    });
    cons.log(" ARGUBOT zegt " +antonyms[hotword]);
  }
});

const mic = record.start({
  threshold: 0,
  verbose: false
});

mic.pipe(detector);
screen.render();

