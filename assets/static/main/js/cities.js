var citiesByState = {
    Andhra_Pradesh: ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Tirupati"],
    Arunachal_Pradesh: ["Itanagar","Tawang", "Bhismaknagar", "Pasighat", "Ziro", "Bomdila"],
    Assam: ["Dispur","Guwahati", "Tezpur", "Dibrugarh", "Silchar", "North Lakhimpur"],
    Bihar: ["Patna","Gaya", "Biharsharif", "Darbhanga", "Bhagalpur"],
    Chhattisgarh: ["Raipur","Bilaspur", "Korba", "Durg-Bhilainagar", "Raigarh", "Rajnandgaon"],
    Goa: ["Panaji","Vasco-da-Gama", "Ponda", "Margao", "Mapusa", "Goa Velha"],
    Gujarat: ["Gandhinagar","Ahmedabad", "Surat", "Rajkot", "Junagadh and Vadodara"],
    Haryana: ["Chandigarh ","Faridabad", "Gurgaon", "Sonipat", "Panipat", "Ambala"],
    Himachal_Pradesh:["Shimla","Dharamshala", "Mandi", "Solan", "Bilaspur", "Chamba"],
    Jharkhand:["Ranchi","Bokaro Steel City", "Jamshedpur", "Deoghar", "Hazaribagh", "Dhanbad"],
    Karnataka: ["Bengaluru","Mysore", "Davangere", "Mangalore", "Hubli-Dharwad", "Belgaum"],
    Kerala: ["Thiruvananthapuram","kochi","Kanpur", "Kozhikode", "Thrissur", "Malappuram"],
    Madhya_Pradesh: ["Bhopal","Indore", "Gwalior", "Jabalpur", "Ujjain", "Sagar"],
    Maharashtra: ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad", "Solapur"],
    Manipur: ["Imphal","Bishnupur", "Ukhrul", "Tamenglong", "Chandel", "Senapati"],
    Meghalaya: ["Shillong","Cherrapunji", "Tura", "Jowai", "Baghmara", "Nongpoh"],
    Mizoram: ["Aizawl","Lunglei", "Serchhip", "Champhai", "Tuipang", "Mamit"],
    Nagaland: ["Kohima","Tuensang", "Zunheboto", "Mokokchung", "Kiphire Sadar", "Phek"],
    Odisha:["Bhubaneswar","Rourkela", "Cuttack", "Brahmapur", "Puri", "Sambalpur"],
    Punjab: ["Chandigarh ","Amritsar", "Jalandhar", "Ludhiana", "Patiala", "Kapurthala"],
    Rajasthan: ["Jaipur","Bikaner", "Jaisalmer", "Jodhpur", "Udaipur", "Ajmer"],
    Sikkim: ["Gangtok","Namchi", "Gyalshing", "Mangan", "Rabdentse"],
    Tamil_Nadu: ["Chennai","Tiruchirappalli", "Madurai", "Erode", "Vellore", "Coimbatore"],
    Telangana: ["Hyderabad","Warangal", "Nizamabad", "Karimnagar", "Adilabad", "Khammam"],
    Tripura: ["Agartala","Amarpur", "Kumarghat", "Udaipur", "Gakulnagar", "Kunjaban"],
    Uttar_Pradesh: ["Lucknow","Noida", "Varanasi", "Allahabad", "Agra", "Kanpur"],
    Uttarakhand:["Dehradun","Haridwar", "Roorkee", "Rishikesh", "Kashipur", "Haldwani"],
    West_Bengal: ["Kolkata","Darjeeling", "Siliguri", "Asansol", "Howrah", "Durgapur"],
    Jammu_and_Kashmir:["Srinagar","Jammu", "Anantnag"],
    Andaman_and_Nicobar_Islands:["Port Blair","Mayabunder", "Alipur", "Andaman Island"],
    Chandigarh: ["Chandigarh", "Khuda Jassu", "Lahora", "Khuda Alisher", "Mani Majra", "Basti Kishangarh", "Basti Bhagwanpura", "Daria", "Mauli Jagran"],

    Dadra_and_Nagar_Haveli: ["Silvassa Municipal Council", "Naroli Census Town", "Dadra Census Town", "Samarvarni Census Town"],
    Daman_and_Diu: ["Municipal Council", "Census Town"],
    Lakshadweep: ["Andrott"],
    National_Capital_Territory_of_Delhi: ["Delhi", "Faridabad", "Ghaziabad", "Gurugram", "Noida"],
    Puducherry: ["Puducherry", "Uzhavarkarai"]

    }
    function makeSubmenu(value) {
    if(value.length==0) document.getElementById("citySelect").innerHTML = "<option></option>";
    else {
    var citiesOptions = "";
    for(cityId in citiesByState[value]) {
    citiesOptions+="<option>"+citiesByState[value][cityId]+"</option>";
    }
    document.getElementById("citySelect").innerHTML = citiesOptions;
    }
    }
    function displaySelected() { var country = document.getElementById("stateSelect").value;
    var city = document.getElementById("citySelect").value;
    alert(country+"\n"+city);
    }
    function resetSelection() {
    document.getElementById("stateSelect").selectedIndex = 0;
    document.getElementById("citySelect").selectedIndex = 0;
    }