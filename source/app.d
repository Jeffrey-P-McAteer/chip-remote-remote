import std.concurrency;
import std.uuid;
import std.algorithm;
import std.json;

import core.thread;
import ddbc;
import vibe.vibe;

bool VERBOSE = false;
Connection dbconn;

void main(string[] args) {
	import std.getopt;
	import std.stdio;
	// Default args
	string db_conn_url = "sqlite:chip_remote_remote.sqlite";
	ushort http_port = 8080;
	string web_assets_dir = "./www/";
	
	// Parse arguments
	auto helpInfo = getopt(
		args,
		"db_conn_url|c",	 "See https://code.dlang.org/packages/ddbc for examples. Creates sqlite db ./chip_remote_remote.sqlite if not specified.", &db_conn_url,
		"verbose|v", 		 "Print additional debugging information", &VERBOSE,
		"http_port|p", 		 "Port HTTP server will listen on", &http_port,
		"web_assets_dir|d",  "Location of static web resources", &web_assets_dir,
	);
	
	if (helpInfo.helpWanted) {
		defaultGetoptPrinter("Usage: "~args[0], helpInfo.options);
		return;
	}
	
	dbconn = createConnection(db_conn_url);
	// the router will match incoming HTTP requests to the proper routes
	auto router = new URLRouter;
	router.registerWebInterface(new WebApp());
	router.get("*", serveStaticFiles(web_assets_dir));
	
	auto settings = new HTTPServerSettings;
	settings.port = http_port;
	settings.bindAddresses = ["0.0.0.0"];
	debug settings.options &= ~HTTPServerOption.errorStackTraces;
	listenHTTP(settings, router);
	runApplication();
}

class WebApp {
	
	void get() {
		render!("index.dt");
	}
	
	void post() {
		render!("index.dt");
	}
	
}
