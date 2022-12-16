// center: {lat: 17.4464, lng: 78.5684 }
function initMap() {
    let mapOptions = {
        center: new google.maps.LatLng('17.4464', '78.5684'),
        zoom: 12,
    }

    let map = new google.maps.Map(document.getElementById('map'),mapOptions);
    
    var icon = {
        url: "./speech2.png", // url
        scaledSize: new google.maps.Size(42, 42), // size
    };
    let locations_list="{{feedback_data}}"
    console.log(locations_list)

    for (i in locations_list){
        // console.log(locations_list[i])
        // var loc = locations_list[i]["name"]
        // console.log(loc)
        let coords0 = locations_list[i]["lat"]
        let coords1 = locations_list[i]["lng"]
        let number = locations_list[i]["number"]
                        console.log(coords0)
        console.log(coords1)
        let markerOptions = {
            position: new google.maps.LatLng(coords0,coords1),
            map:map,
            icon:icon,
            animation: google.maps.Animation.DROP,
            label:{
                text: number,
                color:'#FFFFFF',
                fontSize: '14px',
                fontWeight: 'bolder',
            }
        }

        let marker = new google.maps.Marker(markerOptions)
        //end
    }

}
