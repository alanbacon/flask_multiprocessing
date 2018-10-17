const fetch = require('node-fetch');
const baseUrl = 'http://localhost:8080/';


async function sendReq (id, path) {
	let start = new Date();
	let resp = await fetch(baseUrl + path + id + '?complexity=10000000');
	let body = await resp.text();
	let end = new Date();
	durationSecs = (end - start) / 1000;
	console.log(String(id) + ' node: ' + String(durationSecs) + ' python: ' + body);
}

function sendSyncReqs (reqsToSend) {
	let promises = []
	for (let r=1; r<=reqsToSend; r++) {
		console.log('sending sync request ' + r);
		promises.push(sendReq(r, 'work_sync/'));
	}
	return Promise.all(promises)
}

function sendAsyncReqs (reqsToSend) {
	let promises = []
	for (let r=1; r<=reqsToSend; r++) {
		console.log('sending async request ' + r);
		promises.push(sendReq(r, 'work/'));
	}
	return Promise.all(promises)
}

async function sendSyncRequestThenAsyncRequests(reqsToSend) {
	console.log('send sync requests:')
	let start = new Date();
	await sendSyncReqs(reqsToSend)
	let end = new Date();
	durationSecs = (end - start) / 1000;
	console.log('total node secs: ' + durationSecs)
	console.log(' ')

	start = new Date();
	console.log('send async requests:')
	await sendAsyncReqs(reqsToSend)
	end = new Date();
	durationSecs = (end - start) / 1000;
	console.log('total node secs: ' + durationSecs)
}


// flask app needs to be run in production mode or with threading enabled
// in order to see a difference in response times in it's sync and async 
// endpoints

sendSyncRequestThenAsyncRequests(9)
