fprintf( 'Connecting to Motive\n' );
% create an instance of the natnet client class
global natnetclient;
natnetclient = natnet;

% connect the client to the server (multicast over local loopback) -
% modify for your network

natnetclient.HostIP = '127.0.0.1';
natnetclient.ClientIP = '127.0.0.1';
natnetclient.ConnectionType = 'Multicast';
natnetclient.connect;
if ( natnetclient.IsConnected == 0 )
	fprintf( 'Client failed to connect\n' )
	fprintf( '\tMake sure the host is connected to the network\n' )
	fprintf( '\tand that the host and client IP addresses are correct\n\n' ) 
	return
end

% get the asset descriptions for the asset names
model = natnetclient.getModelDescription;
if ( model.RigidBodyCount < 1 )
	return
end
fprintf( '  Model_Count : "%d" \n', model.RigidBodyCount )

for i = 1:model.RigidBodyCount
	fprintf( '  ->Name : "%s" \n', model.RigidBody( i ).Name )
end
    

%data = natnetclient.getFrame; % method to get current frame
fprintf( 'Connected \n' );