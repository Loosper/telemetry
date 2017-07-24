// declare a new module called 'myApp', and make it require the `ng-admin` module as a dependency
var myApp = angular.module('Telemetry', ['ng-admin']);
// declare a function to run when the module bootstraps (during the 'config' phase)
myApp.config(['NgAdminConfigurationProvider', function (nga) {
    // create an admin application
    var admin = nga.application('Telemetry administration page');
        // .baseApiUrl('http://localhost:5000/');

    var device = nga.entity('devices');
    device.listView().fields([
        nga.field('id'),
        nga.field('delivery_date'),
        nga.field('provider'),
        nga.field('type'),
        nga.field('model'),
        nga.field('serial')
    ]);

    // this is up for debate: should listing show everything or only crucial info?
    device.editionView().fields(device.listView().fields());
    device.creationView().fields(device.listView().fields());
    device.deletionView().fields(device.listView().fields());

    admin.addEntity(device);

    // attach the admin application to the DOM and execute it
    nga.configure(admin);
}]);
