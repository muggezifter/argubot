#! /usr/bin/env node

const exec = require('child_process').exec;
const blessed = require('blessed');
const contrib = require('blessed-contrib');
const record = require('node-record-lpcm16');
const { Models, Detector } = require('snowboy');

const lexicon = {
  ja : {antonym: 'nee', sensitity: 0.5, model: 'ja.pmdl'},
  nee: {antonym: 'ja', sensitity: 0.5, model: 'ja.pmdl'},
  goed : {antonym: 'fout', sensitity: 0.5, model: 'fout.pmdl'},
  fout : {antonym: 'goed', sensitity: 0.5, model: 'goed.pmdl'},
  links : {antonym: 'rechts', sensitity: 0.5, model: 'rechts.pmdl'},
  rechts : {antonym: 'links', sensitity: 0.5, model: 'links.pmdl'},
  zwart : {antonym: 'wit', sensitity: 0.5, model: 'wit.pmdl'},
  wit : {antonym: 'zwart', sensitity: 0.5, model: 'zwart.pmdl'}
}

const screen = blessed.screen({
  smartCSR: true,
});

const bg = blessed.box({
  left: 0,
  top: 0,
  width: '100%',
  height: '100%',
  style: {
    bg: "#0000ff"
  }
});

const cons = contrib.log({
  label: 'CONSOLE',
  border: {
    type: 'line'
  },
  width: '80%',
  height: '15%',
  top: '70%',
  left: 'center',
  style:{
     bg: [0,0,255],
     fg: [255,255,255],
     border : {
      bg: [0,0,255],
      fg: [0,255,0]
     },
     label : {
      bg: [0,0,255],
      fg: [0,255,0]
     }
  }
})

const wave = contrib.line({
  label: 'AUDIO',
  border: {
    type: 'line'
  },
  top: '10%',
  width: '80%',
  height: '60%',
  padding: { top: 1, bottom: 0, left: 0, right: 0},
  left: 'center',
  numYLabels: 5,
  style:{
    bg: [0,0,255],
     line: [255,255,0],
     baseline: [127,127,127],
     border : {
      bg: [0,0,255],
      fg: [0,255,0]
     },
     label : {
      bg: [0,0,255],
      fg: [0,255,0]
     }
  }
})

const create_bt = function(message) {
  return blessed.bigtext({
    content: ' ' + message + ' ',
    border: { type: 'line' },
    padding: { top: 1, bottom: 1, left: 0, right:  2},
    width: 'shrink',
    left: 'center',
    top: 'center',
    height: 20,
    style: {
      shadow: true,
      bg: '#ff0000',
      fg: '#ffffff',
      border: { fg: '#ffffff', bg: '#ff0000'}
    }
  });
}

screen.append(bg);
screen.append(wave);
screen.append(cons);

const wave_x = [...Array(86).keys()];

wave.setData([{
  x: wave_x,
  y: wave_x.map(v=>127+127*Math.sin(v*5*Math.PI/86))
}])

const models = new Models();

for (hotword in lexicon) {
  models.add({
    file: '../models/snowboy/'+ lexicon[hotword].model,
    sensitivity: lexicon[hotword].sensitity,
    hotwords : hotword
  });
}

const detector = new Detector({
  resource: './node_modules/snowboy/resources/common.res',
  models: models,
  audioGain: 2.0
});

var argubot_is_speaking = false;
var cnt_silence = 0;
var dots='';
detector.on('silence', function () {
  if (++cnt_silence > 5 && ! argubot_is_speaking) {
    cons.log(' ARGUBOT luistert' + dots);
    if (dots.length == 5) cons.log(' [Ctrl-c om af te sluiten]');
    dots = (dots.length < 5)? dots+'.' : '';
    cnt_silence = 0;
  }
});

detector.on('sound', function (buffer) {
  if (argubot_is_speaking) return;
  cons.log(' ARGUBOT analyseert buffer...');
  setTimeout(()=>{
    const offset = Math.floor(buffer.length/4);
    const smpls = buffer.filter((v,i)=>i%2==0).slice(offset,offset+86);
    wave.setData([ {
     x: wave_x,
     y: smpls
    }])},
  100)
});

detector.on('error',()=>cons.log(' error'));

detector.on('hotword', function (index, hotword, buffer) {
  if (! argubot_is_speaking) {
    cons.log(' >>> U zegt "' + hotword + '"');
    argubot_is_speaking = true;
    const bt = create_bt(lexicon[hotword].antonym);
    screen.append(bt);
    setTimeout(()=>bt.destroy(),50);
    exec('espeak -vnl+m2 ' + lexicon[hotword].antonym , function (error, stdout, stderr){
      setTimeout(()=>argubot_is_speaking=false,500);
    });
    cons.log(' >>> ARGUBOT zegt "' + lexicon[hotword].antonym + '"');
  }
});

const mic = record.start({
  threshold: 0,
  verbose: false
});

mic.pipe(detector);
screen.render();
