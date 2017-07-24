// declare a new module called 'myApp', and make it require the `ng-admin` module as a dependency
var myApp = angular.module('Telemetry', ['ng-admin']);
// declare a function to run when the module bootstraps (during the 'config' phase)
myApp.config(['NgAdminConfigurationProvider', function (nga) {
    // create an admin application
    var admin = nga.application('Telemetry administration page');
        // .baseApiUrl('http://localhost:5000/');

    // TODO: input validation
    var device = nga.entity('devices');
    var sim = nga.entity('sims');
    var couple = nga.entity('couples');

    device.listView().fields([
        nga.field('id'),
        nga.field('delivery_date'),
        nga.field('provider'),
        nga.field('type'),
        nga.field('model'),
        nga.field('serial')
    ]);

    sim.listView().fields([
        nga.field('id'),
        nga.field('delivery_date'),
        nga.field('carrier'),
        nga.field('number')
    ]);

    couple.listView().fields([
        nga.field('id'),
        nga.field('couple_date'),
        nga.field('device_id', 'reference').
            targetEntity(device).targetField(nga.field('id')),
        nga.field('sim_id', 'reference').
            targetEntity(sim).targetField(nga.field('id')),
        nga.field('assigned_to')
    ]);

    // REVIEW: which method should show what?
    device.editionView().fields(device.listView().fields());
    device.creationView().fields(device.listView().fields());
    device.deletionView().fields(device.listView().fields());

    sim.editionView().fields(sim.listView().fields());
    sim.creationView().fields(sim.listView().fields());
    sim.deletionView().fields(sim.listView().fields());

    couple.editionView().fields(couple.listView().fields());
    couple.creationView().fields(couple.listView().fields());
    couple.deletionView().fields(couple.listView().fields());

    admin.addEntity(device);
    admin.addEntity(sim);
    admin.addEntity(couple);

    // attach the admin application to the DOM and execute it
    nga.configure(admin);
}]);
