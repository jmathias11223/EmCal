//package javafiles;

import java.util.HashMap;
/**
 * Class for handling all calculations
 * 
 * @author Justin Mathias
 * @version 2021.05.19
 */
public class Calculate {

    private static HashMap<String, Double> metTableWalking;
    private static HashMap<String, Double> metTableBiking;
    private static double mostRecentCalsBurned; // Most recent calories burned value from calculateWalkOrBikeC02Emissions

    // Main method; purely for testing
    public static void main(String[] args) {
        System.out.println(calculateWalkOrBikeC02Emissions(1, VehicleType.BIKE, 0.05, 190));
    }

    /**
     * Calculates C02 emissions in g/mile based on MPG
     * 
     * @param mileage MPG value
     * @return C02 emissions in g/mile
     */
    public static double calculateC02Emissions(double mileage) {
        return (8.8 / mileage) * 1000.0;
    }

    /**
     * Calculates the monetary cost of a trip with your personal vehicle
     * 
     * @param mileage MPG value
     * @param distance Total distance of trip, in miles
     * @param gasPrice Price of gas per gallon, in USD
     * @return Total trip cost
     */
    public static double calculateTripCost(double mileage, double gasPrice, double distance) {
        double gallonsUsed = distance / mileage;
        double price = gallonsUsed * gasPrice;
        return price;
    }

    /**
     * Calculates the estimated average speed of the vehicle 
     * 
     * @param cityMileage City MPG
     * @param highwayMileage Highway MPG
     * @param distance Total distance of trip, in miles
     * @param time Total time for the trip, in hours
     * @return Average mileage for the vehicle
     */
    public static double calculateAverageMPG(int cityMileage, int highwayMileage, double distance, double time) {
        double avgSpeed = distance / time;      // Miles per hour
        double cityPercentage = Math.abs(60 - avgSpeed) / 40;
        double highwayPercentage = 1 - cityPercentage;
        double avgMPG = cityMileage * cityPercentage + highwayMileage * highwayPercentage;
        if(avgMPG > highwayMileage) {
            return (double)highwayMileage;
        }
        else if(avgMPG < cityMileage) {
            return (double)cityMileage;
        }
        return avgMPG;
    }

    /**
     * Source: https://www.globe.gov/explore-science/scientists-blog/archived-posts/sciblog/index.html_p=186.html
     * 0.7 kg of C02 released for every 2000 kCal burned by people
     * 
     * Source: https://www.hss.edu/conditions_burning-calories-with-exercise-calculating-estimated-energy-expenditure.asp
     * Formula for calories burned = 0.0175 * MET * weight(kg) * time(in minutes)
     * 
     * @param distance
     * @param type
     * @param time in hrs
     * @param weight in lbs
     * @return
     */
    public static double calculateWalkOrBikeC02Emissions(double distance, VehicleType type, double time, double weight) {
        double speed = distance / time;
        double met = 0;
        double emissions = 0;
        if(metTableWalking == null) {
            instantiateHashMaps();
        }
        switch(type) {
            case WALK:
                double[] speeds = {2.0, 2.5, 3.0, 4.0, 4.5};
                for(int i = 0; i < speeds.length; i++) {
                    if(speed < speeds[i]) {
                        if(i == 0) {
                            met = speeds[0];
                        }
                        else {
                            met = speeds[i - 1];
                        }
                    }
                }
                if(met == 0) {
                    met = speeds[4];
                }
                met = metTableWalking.get(Double.toString(met));
                break;
            
            case BIKE:
                double[] speeds2 = {10.0, 12.0, 14.0, 16.0, 19.0, 20.0};
                for(int i = 0; i < speeds2.length; i++) {
                    if(speed < speeds2[i]) {
                        if(i == 0) {
                            met = speeds2[0];
                        }
                        else {
                            met = speeds2[i - 1];
                        }
                    }
                }
                if(met == 0) {
                    met = speeds2[5];
                }
                met = metTableBiking.get(Double.toString(met));
                break;

            default:
                System.out.println("If this message prints to console, something is seriously wrong.");
                break;
        }
        double calories = 0.0175 * met * (weight / 2.2) * (time * 60);
        mostRecentCalsBurned = calories;
        emissions = 0.7 / 2000 * calories * 1000; // in grams
        return emissions;
    }

    /**
     * Instantiates and fills the necessary hash maps
     */
    private static void instantiateHashMaps() {
        metTableWalking = new HashMap<String, Double>(5);
        metTableBiking = new HashMap<String, Double>(6);
        metTableWalking.put("2.0", 2.5);
        metTableWalking.put("2.5", 3.0);
        metTableWalking.put("3.0", 3.5);
        metTableWalking.put("4.0", 4.0);
        metTableWalking.put("4.5", 4.5);
        metTableBiking.put("10.0", 4.0);
        metTableBiking.put("12.0", 6.0);
        metTableBiking.put("14.0", 8.0);
        metTableBiking.put("16.0", 10.0);
        metTableBiking.put("19.0", 12.0);
        metTableBiking.put("20.0", 16.0);
    }

    /**
     * Returns the most recent calories burned value from the previous
     * call to calculateWalkOrBikeC02Emissions()
     * 
     * @return Most recent calories burned
     */
    public static double getMostRecentCalsBurned() {
        return mostRecentCalsBurned;
    }
}