
/**
 * Module dependencies.
 */

var express = require('express')
  , app = express()
  , http = require('http')
  , server = http.createServer(app)
  , path = require('path')
  , routes = require('./routes')
  , user = require('./routes/user')
  , io = require('socket.io').listen(server)


var clients = {};
var connectCounter = 0;


server.listen(7777,"0.0.0.0")  ;
console.log('Server running at http://127.0.0.1:7777/');

app.configure(function(){
  app.set('port', process.env.PORT || 7777);
  app.set('views', __dirname + '/views');
  app.set('view engine', 'jade');
  app.use(express.favicon());
  app.use(express.logger('dev'));
  app.use(express.bodyParser());
  app.use(express.methodOverride());
  app.use(app.router);
  app.use(express.static(path.join(__dirname, 'public')));
});

app.configure('development', function(){
  app.use(express.errorHandler());
});

app.get('/', routes.index);
app.get('/users', user.list); 


// TODO: Should this be the main interval loop of a short time
// like 100ms and then trigger different events at different time
// periods. ping at 1 second. check for heartbeat at 500ms etc. 
setInterval(function() {
		ts =  Math.round(new Date().getTime() / 1000);
		console.log('[Sending PING. ' +  ts + ' ]' + '[ ' + connectCounter + ' clients connected.]');

		io.sockets.emit('ping',ts);
			
	},500); 




io.sockets.on('connection',function(socket) {
	console.log('Connection Received. Socket ID: ' + socket.id);
	clients[socket.id] = socket;
	connectCounter++;
	
	socket.on('pong',function(data) {
		console.log('[Received PONG.]');
	});
	socket.on('subscribe', function(roomNumber) { 
		
		socket.join(roomNumber);
		console.log('Socket joined room: ' + roomNumber) 
		//sendConfiguration(socket,roomNumber);
	});
	socket.on('unsubscribe', function(roomNumber) { 
		socket.leave(roomNumber);
		console.log('Socket left room: ' + roomNumber) 
		//sendERROR(socket,"Something went very very wrong!");
	});
	socket.on('configuration', function(data) { 
		// Make sure the client is connected to a room. If not, send error.
		console.log('----Config--Config--Config--Config----');

		//console.log('Socket requested configuration. Will send this data: ' + JSON.stringify(roomData[data]) + ' For room ' + data);
		//sendConfiguration(socket,data);
	});

	socket.on('drive', function(data) { 
		console.log('---> DRIVING. Direction: ' + data.direction + " Speed: " + data.speed); 
	});

	socket.on('dome', function(data) { 
		console.log('---> DOME ROTATING. Direction: ' + data.direction); 
	});


	socket.on('playSound', function(data) { 
		console.log('Playing Sound: ' + data.name); 
	});


	socket.on('disconnect', function () {
        connectCounter--;
    });



});