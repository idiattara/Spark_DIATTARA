public static String processJson(String jsonString) {
        JSONObject jsonObject = new JSONObject(jsonString);
        JSONArray dataArray = jsonObject.getJSONArray("data");
        JSONObject firstEntry = dataArray.getJSONObject(0);
        JSONObject clientProperties = firstEntry.getJSONObject("properties-client");
        JSONObject driverProperties = firstEntry.getJSONObject("properties-driver");

        // Extraction des coordonnées
        double clientLongitude = clientProperties.getDouble("logitude");
        double clientLatitude = clientProperties.getDouble("latitude");
        double driverLongitude = driverProperties.getDouble("logitude");
        double driverLatitude = driverProperties.getDouble("latitude");

        // Calcul de la distance
        double distance = calculateDistance(clientLatitude, clientLongitude, driverLatitude, driverLongitude);

        // Arrondissement de la distance à 3 chiffres après la virgule
        BigDecimal roundedDistance = new BigDecimal(distance).setScale(3, RoundingMode.HALF_UP);

        // Extraction du prix par km
        double prixBasePerKm = firstEntry.getDouble("prix_base_per_km");

        // Calcul du prix total du voyage
        BigDecimal prixTravel = new BigDecimal(prixBasePerKm).multiply(new BigDecimal(roundedDistance.toString()));

        // Modification du JSON pour inclure "location", "distance", et "prix_travel"
        clientProperties.remove("logitude");
        clientProperties.remove("latitude");
        driverProperties.remove("logitude");
        driverProperties.remove("latitude");

        String clientLocation = clientLongitude + ", " + clientLatitude;
        String driverLocation = driverLongitude + ", " + driverLatitude;

        clientProperties.put("location", clientLocation);
        driverProperties.put("location", driverLocation);

        firstEntry.put("distance", roundedDistance);
        firstEntry.put("prix_travel", prixTravel.setScale(2, RoundingMode.HALF_UP));

        return jsonObject.toString(4); // Retourne le JSON modifié en format lisible
    }

    // Méthode pour calculer la distance en utilisant la formule de Haversine
    public static double calculateDistance(double lat1, double lon1, double lat2, double lon2) {
        double dLat = Math.toRadians(lat2 - lat1);
        double dLon = Math.toRadians(lon2 - lon1);

        double a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(Math.toRadians(lat1)) * Math.cos(Math.toRadians(lat2)) *
                        Math.sin(dLon / 2) * Math.sin(dLon / 2);

        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

        return EARTH_RADIUS * c;
    }
