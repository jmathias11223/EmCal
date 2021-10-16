//package javafiles;

/**
 * This object will store each instance of a route, as
 * well as the data associated with each route, from one
 * location to another.
 * 
 * @author Justin Mathias
 * @version 2021.05.19
 */
public class Trip {
    private VehicleType transport;
    private double distance;
    private double avgMPG;
    private String tripCosts;
    private double c02Emissions;
    private double caloriesBurned;
    private String time;

    // Default constructor
    public Trip() {
        transport = VehicleType.MOTOR_VEHICLE;
        distance = 0;
        avgMPG = 0;
        tripCosts = "";
        c02Emissions = 0;
        caloriesBurned = 0;
        time = "";
    }

    // Constructor with all data fields filled in
    public Trip(VehicleType type, double dist, double averageMPG, double sourceCost, double destCost, double c02Ems, double cals, String mTime) {
        transport = type;
        distance = dist;
        avgMPG = averageMPG;
        tripCosts = convertCosts(sourceCost, destCost);
        c02Emissions = c02Ems;
        caloriesBurned = cals;
        time = mTime;
    }

    /**
     * Converts the cost of gas if filled up at the source
     * and destination to a formatted String object
     * 
     * @param source Total cost of gas if filled up at initial location, in USD
     * @param dest Total cost of gas if filled up at the destination, in USD
     * @return Formatted String with both costs
     */
    private String convertCosts(double source, double dest) {
        if(transport != VehicleType.MOTOR_VEHICLE) {
            return "";
        }
        return String.format("Your trip will cost an estimated $%.2f if you fill up gas at your " +
            "initial location.\nYour trip will cost an estimated $%.2f if you fill up gas at your destination.", source, dest);
    }

    /**
     * Returns the mode of transportation
     * 
     * @return A VehicleType enum representing mode of transport
     */
    public VehicleType getTransportType() {
        return transport;
    }

    /**
     * Returns the total distance of the trip
     * 
     * @return Total distance, in miles
     */
    public double getDistance() {
        return distance;
    }

    /**
     * Returns the average mileage of the vehicle in use, if applicable.
     * Returns -1 if not applicable;
     * 
     * @return Average mileage across the trip, in miles per gallon
     */
    public double getAverageMileage() {
        if(transport != VehicleType.MOTOR_VEHICLE) {
            return -1;
        }
        return avgMPG;
    }

    /**
     * Returns the formatted String containing the total cost of
     * the trip based on if gas was filled up at the initial
     * location or at the destination.
     * 
     * @return Formatted String of the total estimated trip cost
     */
    public String getTripCosts() {
        return tripCosts;
    }

    /**
     * Returns the estimated amount of C02 emissions resulting
     * from the trip.
     * 
     * @return Estimated amount of C02 emissions, in grams
     */
    public double getC02Emissions() {
        return c02Emissions;
    }

    /**
     * Returns the amount of calories burned on this trip.
     * 
     * @return Amount of calories burned on this trip
     */
    public double getCaloriesBurned() {
        return caloriesBurned;
    }

    /**
     * Returns the estimated amount of time the trip will take.
     * 
     * @return Estimated time of the trip
     */
    public String getTime() {
        return time;
    }

    /**
     * Modifies the mode of transportation associated with the trip.
     * 
     * @param type New mode of transport
     */
    public void setTransportType(VehicleType type) {
        transport = type;
    }

    /**
     * Modifies the total distance of the trip.
     * 
     * @param dist New total distance value, in miles
     */
    public void setDistance(double dist) {
        distance = dist;
    }

    /**
     * Modifies the average mileage of the vehicle used on this trip.
     * 
     * @param avgMileage New average mileage value, in MPG
     */
    public void setAverageMileage(double avgMileage) {
        avgMPG = avgMileage;
    }

    /**
     * Modifies the formatted String representing total trip costs by
     * inputting two new total trip cost values based on initial location
     * and destination gas prices.
     * 
     * @param src Total trip cost based on gas prices at the initial location, in USD
     * @param dest Total trip cost based on gas prices at the destination, in USD
     */
    public void setTripCosts(double src, double dest) {
        tripCosts = convertCosts(src, dest);
    }

    /**
     * Modifies the total amount of C02 emissions resulting from this trip.
     * 
     * @param c02Ems New value for C02 emissions, in grams
     */
    public void setC02Emissions(double c02Ems) {
        if(transport == VehicleType.AIRPLANE) {
            c02Ems *= 1000000;
        }
        c02Emissions = c02Ems;
    }

    /**
     * Modifies the total amount of calories burned
     * 
     * @param cals New amount of calories burned
     */
    public void setCaloriesBurned(double cals) {
        caloriesBurned = cals;
    }

    /**
     * Modifies the total time taken for this trip
     * 
     * @param t New time for trip
     */
    public void setTime(String t) {
        time = t;
    }

    @Override
    public String toString() {
        boolean air = false;
        StringBuilder str = new StringBuilder();
        str.append("Information about this trip: \n");
        String mode = null;
        switch(transport) {
            case MOTOR_VEHICLE:
                mode = "Motor vehicle";
                break;
            
            case AIRPLANE:
                mode = "Airplane";
                air = true;
                break;
            
            case WALK:
                mode = "Walking";
                break;
            
            case BIKE:
                mode = "Bicycling";
                break;
            
            default:
                mode = null;
                break;
        }
        if(air && c02Emissions == 0) {
            str.append("There is no flight option available for the selected locations.");
            return str.toString();
        }
        str.append(String.format("Mode of transportation: %s\n", mode));
        str.append(String.format("Total distance: %.2f miles\n", distance));
        str.append(String.format("Total time: %s\n", time));
        if(transport != VehicleType.MOTOR_VEHICLE) {
            str.append("Average Mileage: N/A\n");
        }
        else {
            str.append(String.format("Average Mileage: %.2f MPG\n", avgMPG));
        }
        str.append(String.format("Total C02 Emissions: %.2f grams\n", c02Emissions));
        if(caloriesBurned <= 0) {
            str.append("Total Calories Burned: N/A\n");
        }
        else {
            str.append(String.format("Total Calories Burned: %.2f kCal\n", caloriesBurned));
        }
        str.append(tripCosts + "\n");
        return str.toString();
    }
}
