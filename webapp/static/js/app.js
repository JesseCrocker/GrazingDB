var app = angular.module('grazingdb', [ 'ngResource' ]);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});

function ListController($scope, $resource) {
    $scope.predicate = 'name';
    
    var Allotment = $resource('/api/allotments/:uid',
     {uid:'@uid'},
     {
        update: { method: 'PUT', params:{uid:'@uid'} },
        get: { method: "GET" } }
     );

    Allotment.query({}, function (response, headers) {
           $scope.items = response; 
    });

    $scope.toggleInvolved = function($event, item) {
        var input = $event.target;
        item.involved = input.checked;
        item.$update({uid:item.id});
    };
};

function MapController($scope, $resource) {
    $scope.predicate = 'name';
    
    var Allotment = $resource('/api/geo/allotments/:uid',
     {uid:'@uid'},
     {
        update: { method: 'PUT', params:{uid:'@uid'} },
        get: { method: "GET" } }
     );

    $scope.initMap = function init(){
        OpenLayers.ImgPath = "/static/img/openlayers/";
        $scope.map = new OpenLayers.Map( 'map', {
            'theme':null,
            controls: [
                        new OpenLayers.Control.Navigation(),
                        new OpenLayers.Control.PanZoomBar(),
                        new OpenLayers.Control.KeyboardDefaults(),
                        new OpenLayers.Control.LayerSwitcher({
                            'ascending':false
                        }),
                        new OpenLayers.Control.ScaleLine({
                        }),
                    ]
        });
        layer = new OpenLayers.Layer.OSM( "Open Street Map");
        $scope.map.addLayer(layer);
        $scope.map.setCenter(
            new OpenLayers.LonLat(-115, 40).transform(
                new OpenLayers.Projection("EPSG:4326"),
                $scope.map.getProjectionObject()
            ), 5
        );
        $scope.polyLayer = new OpenLayers.Layer.Vector( "Allotments", {} );
        $scope.map.addLayer($scope.polyLayer);

        $scope.markerLayer = new OpenLayers.Layer.Markers( "Allotment Markers", {} );
        $scope.markerLayer.visibility = false;
        $scope.map.addLayer($scope.markerLayer);
    };

    Allotment.query({}, function (response, headers) {
        $scope.items = response;

        involved_style = { 
                'strokeWidth': 2,
                'strokeColor': 'green',
                //'fillColor': '#E6DB74',
                'fillOpacity': 0.1,
        };
        non_involved_style = { 
                'strokeWidth': 2,
                'strokeColor': '#ff0000',
                //'fillColor': '#E6DB74',
                'fillOpacity': 0.1,
        };
        var iconSize = new OpenLayers.Size(21,25);
        var iconOffset = new OpenLayers.Pixel(-(iconSize.w/2), -iconSize.h);
        var icon = new OpenLayers.Icon('http://www.openlayers.org/dev/img/marker.png',iconSize,iconOffset);

        var mercator = new OpenLayers.Projection("EPSG:900913");
        var geographic = new OpenLayers.Projection("EPSG:4326");

        var wktReader = new OpenLayers.Format.WKT();

        for ( var i = 0; i < $scope.items.length; i++) {
            var item = $scope.items[i];
            var feature = wktReader.read(item.geometry);
            feature.geometry.transform(geographic, mercator);
            if(item.involved) {
                feature.style = involved_style;
            } else {
                feature.style = non_involved_style;
            }
   
            $scope.polyLayer.addFeatures(feature);
 
            var centroid = feature.geometry.getCentroid()
            point = new OpenLayers.LonLat(centroid.x, centroid.y);
            marker = new OpenLayers.Marker(point);
            $scope.markerLayer.addMarker(marker);
        }
        var dataExtent = $scope.polyLayer.getDataExtent();
        $scope.map.zoomToExtent(dataExtent, true);
    });

    $scope.initMap();
};
