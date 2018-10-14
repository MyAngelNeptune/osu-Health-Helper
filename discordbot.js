const Discord = require("discord.js");
const client = new Discord.Client();
const config = require("./config.json");
const fs = require("fs"); //Load the filesystem module
const stats = fs.statSync("./remind.txt");

var osu = "OSU HEALTH REMINDER:" +
"You have reached your designated Time and BPM thresholds." +
"Now would be a great time to consider taking a break and stretching." +
"Are you in pain? Y\N"

var myPythonScriptPath = './osu_health_watcher.py';
const spawn = require("child_process").spawn;
const pythonProcess = spawn('python',[myPythonScriptPath]);
var general = client.channels.find('name', 'general')

client.login(config.key);
 everything()

function everything(){
  client.on("ready", () => {
    console.log("I am ready!");

  });

  client.on("message", (message) => {
    general = message.channel;
  });

  function display(){
    var stats = fs.statSync("./remind.txt");
    if(stats.size != 0){
      general.send(osu);
      fs.truncate('./remind.txt', 0, function(){console.log('done')})
    }
  }
  display();
  sleep(5000).then(() => {
      everything()
  })
}





function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}
