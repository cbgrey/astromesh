
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


server.listen(7777)  ;
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

setInterval(function() {
		console.log('[Sending PING.]');
		io.sockets.emit('ping',{text:'PING'});
			
	},6000); 




io.sockets.on('connection',function(socket) {
	console.log('Connection Received. Socket ID: ' + socket.id);
	clients[socket.id] = socket;
	
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
});