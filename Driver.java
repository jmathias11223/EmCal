//package javafiles;

import java.io.*;
import java.util.HashMap;
import java.util.Scanner;

/**
 * Main class that handles all back-end calculations
 * 
 * @author Justin Mathias
 * @version 2021.05.19
 */
public class Driver {

    private static HashMap<String, String> dtMap;
    private static double c02EmsFlight;
    
    /**
     * Purely for testing purposes
     */
    public static void main(String[] args) throws IOException {
        String[] arr = new String[0];
        run(arr, VehicleType.MOTOR_VEHICLE);
    }

    /**
     * Main run method; called from UI class
     * 
     * @param params All inputs from UI:
     *                  For motor vehicles:
     *                      args[0] = Initial location address
     *                      args[1] = Final destination address
     *                      args[2] = Vehicle make
     *                      args[3] = Vehicle model
     *                      args[4] = Vehicle year
     *                      args[5] = Vehicle fuel type
     *                  For walking/biking:
     *                      args[0] = Initial location
     *                      args[1] = Destination
     *                      args[2] = User weight
     *                  For public transit:
     *                      args[0] = Initial location
     *                      args[1] = Final destination
     * @param type Vehicle type used(Mode of transportation)
     * @return All output info for the specified vehicle type and route in a Trip object
     * 
     * Note: Refer to the Trip.java class for information on the methods and fields in it
     */
    public static Trip run(String[] params, VehicleType type) throws IOException {
        // Used mostly for testing purposes
        String[] arr;
        if(params.length != 0) {
            arr = params;
        }
        else {
            arr = new String[8];
            //arr[0] = "15040 Conference Center Dr #210, Chantilly, VA, USA";
            arr[0] = "100 Universal City Plaza, Universal City, CA, USA";
            arr[1] = "1 center court, Cleveland, OH, USA";
            //arr[1] = "4201 Stringfellow Rd, Chantilly, VA, USA";
            arr[2] = "Nissan";
            arr[3] = "Altima";
            arr[4] = "2018";
            arr[5] = "Regular";
            arr[6] = "35";
            arr[7] = "150"; // Weight

            // For if we don't get Maven to work
            Scanner readInp = new Scanner(System.in);
            System.out.println("Please enter the address of your starting location:");
            arr[0] = readInp.nextLine();
            System.out.println("Please enter the address of your destination:");
            arr[1] = readInp.nextLine();
            System.out.println("Please enter your vehicle's make, model, and year:(e.g. Nissan Altima 2021)");
            String[] car = readInp.nextLine().split(" ");
            arr[2] = car[0];
            arr[3] = car[1];
            arr[4] = car[2];
            System.out.println("Please enter your vehicle's mileage, in MPG:");
            arr[6] = readInp.next();
            System.out.println("Please enter your vehicle's fuel type:(e.g. Regular)");
            arr[5] = readInp.next();
            System.out.println("Please enter your weight, in pounds:");
            arr[7] = readInp.next();
            System.out.println("Please enter the mode of transportation(Must be Walking, Biking, Airplane, or Car):");
            String mode = readInp.next();
            switch(mode) {
                case "Walking":
                    type = VehicleType.WALK;
                    break;

                case "Biking":
                    type = VehicleType.BIKE;
                    break;

                case "Airplane":
                    type = VehicleType.AIRPLANE;
                    break;

                default:
                    type = VehicleType.MOTOR_VEHICLE;
                    break;
            }
            readInp.close();
        }

        // Run scrape_flight_c02.py first
        String[] flCmd = {"python3", "pythonfiles/scrape_flight_co2.py", arr[0], arr[1]};
        Runtime rt = Runtime.getRuntime();
        try {
            rt.exec(flCmd);
        }
        catch(Exception ex) {
            System.out.println("Didn't work :(");
            System.exit(0);
        }
        File flights = new File("datafiles/flight_co2_emission.csv");
        Scanner flightScan = new Scanner(flights);
        flightScan.useDelimiter(",");
        String src = flightScan.next();
        String dest = flightScan.next();
        arr[0] = arr[0] + "; " + src;
        arr[1] = arr[1] + "; " + dest;
        String ems = flightScan.next();
        if(ems.contains("N/A")) {
            c02EmsFlight = 0;
        }
        else {
            Scanner sc = new Scanner(ems);
            c02EmsFlight = sc.nextDouble();
            sc.close();
        }
        flightScan.close();

        // Grab distance and time data
        String[] cmd = {"python3", "pythonfiles/scrape_distance_and_time.py", arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6]};
        Runtime currRunObj = Runtime.getRuntime();
        String error = "error";
        Process pr = null;
        while(error != null && !error.equals("")) {
            try {
                pr = currRunObj.exec(cmd);
            }
            catch(Exception ex) {
                System.out.println("Didn't work :(");
                System.exit(0);
            }
            BufferedReader errorRead = new BufferedReader(new InputStreamReader(pr.getErrorStream()));
            error = errorRead.readLine();
        }
        

        // Build HashMap of distance/time data
        File dtData = new File("datafiles/travel_distance_and_time.csv");
        Scanner fileScanner = new Scanner(dtData);
        dtMap = new HashMap<String, String>();
        String str = null;
        while((str = fileScanner.nextLine()) != null) {
            if(!str.equals("")) {
                String[] tokens = str.split(",");
                dtMap.put(tokens[0], tokens[1] + "," + tokens[2]);
            }
            if(!fileScanner.hasNext()) {
                break;
            }
        }
        fileScanner.close();

        // Call the appropriate run() variation method based on mode of transportation
        switch(type) {
            case MOTOR_VEHICLE:
                return runMotorVehicle(params);

            case WALK:
                return runWalkOrBike(params, type);

            case BIKE:
                return runWalkOrBike(params, type);

            case AIRPLANE:
                return runAirplane(params);

            default:
                return null;
        }
    }

    /**
     * Given user input, this method provides a Trip object with
     * all relevant output information for motor vehicle transport.
     * 
     * @param params User input array
     * @return Trip object with all relevant output information for motor vehicles
     * @throws IOException
     */
    public static Trip runMotorVehicle(String[] params) throws IOException {
        // More testing code
        String[] arr;
        if(params.length != 0) {
            arr = params;
        }
        else {
            arr = new String[7];
            arr[0] = "15040 Conference Center Dr #210, Chantilly, VA 20151";
            arr[1] = "25450 Riding Center Dr, Chantilly, VA 20152";
            arr[2] = "Nissan";
            arr[3] = "Altima";
            arr[4] = "2018";
            arr[5] = "Regular";
            arr[6] = "35";
        }

        // Read data from .csv file
        String data = dtMap.get("Driving");
        String[] tkns = data.split(",");
        double distance = Double.parseDouble(tkns[0]);
        String time = tkns[1];

        // Grab gas price data
        String[] cmd = {"python3", "pythonfiles/scrape_gas_info_2.0.py", arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6]};
        Runtime currRunObj = Runtime.getRuntime();
        try {
            currRunObj.exec(cmd);
        }
        catch(Exception ex) {
            System.out.println("Didn't work :(");
            System.exit(0);
        }
        
        // Check if gas prices web scraping worked
        File gas = new File("datafiles/gas_prices.csv");
        Scanner gasSc = new Scanner(gas);
        String[] line = gasSc.nextLine().split(",");
        double srcPrice = Double.parseDouble(line[0]);
        double destPrice = Double.parseDouble(line[1]);
        gasSc.close();

        // Grab mileage data; not necessary anymore
        //
        // int cityMileage = 0;
        // int highwayMileage = 0;
        // String[] cmd3 = {"python3", "pythonfiles/scrape_milage_info.py", arr[2], arr[3], arr[4]};
        // currRunObj = Runtime.getRuntime();
        // Process proc = null;
        // try {
        //     proc = currRunObj.exec(cmd3);
        // }
        // catch(Exception ex) {
        //     System.out.println("Didn't work :(");
        //     System.exit(0);
        // }
        // BufferedReader inp = new BufferedReader(new InputStreamReader(proc.getInputStream()));
        // String[] mileages = inp.readLine().split(",");
        // highwayMileage = Integer.parseInt(mileages[0]);
        // cityMileage = Integer.parseInt(mileages[1]);
        // System.out.println(highwayMileage);
        // System.out.println(cityMileage);

        // Perform all calculations
        //double convertedTime = convertTime(time);
        double avgMPG = Double.parseDouble(arr[6]);
        double sourceCost = Calculate.calculateTripCost(avgMPG, srcPrice, distance);
        double destCost = Calculate.calculateTripCost(avgMPG, destPrice, distance);
        double c02Emissions = Calculate.calculateC02Emissions(avgMPG) * distance;

        // Putting all relevant information into a Trip object
        Trip trip = new Trip(VehicleType.MOTOR_VEHICLE, distance, avgMPG, sourceCost, destCost, c02Emissions, 0, time);
        System.out.println(trip.toString());
        return trip;
    }

    /**
     * Given user input, this method returns a Trip object with all the necessary
     * output data for walking or bicycling.
     * 
     * @param params User input
     * @param type Mode of transportation
     * @return A Trip object with all relevant output data
     * @throws FileNotFoundException
     */
    public static Trip runWalkOrBike(String[] params, VehicleType type) throws FileNotFoundException {
        Trip trip = new Trip();
        trip.setAverageMileage(-1);
        trip.setTransportType(type);
        
        // Pull data from arguments
        String[] arr;
        if(params.length != 0) {
            arr = params;
        }
        else {
            arr = new String[8];
            arr[0] = "15040 Conference Center Dr #210, Chantilly, VA 20151";
            arr[1] = "25450 Riding Center Dr, Chantilly, VA 20152";
            arr[7] = "150";
        }
    

        // Calculate values
        if(type == VehicleType.WALK) {
            String[] vals = dtMap.get("Walking").split(",");
            double dist = Double.parseDouble(vals[0]);
            double time = convertTime(vals[1]);
            trip.setDistance(dist);
            trip.setTripCosts(0, 0);
            trip.setTime(vals[1]);
            trip.setC02Emissions(Calculate.calculateWalkOrBikeC02Emissions(dist, type, time, Double.parseDouble(arr[7])));
            trip.setCaloriesBurned(Calculate.getMostRecentCalsBurned());
        }
        else {
            String[] vals = dtMap.get("Bicycling").split(",");
            double dist = Double.parseDouble(vals[0]);
            double time = convertTime(vals[1]);
            trip.setDistance(dist);
            trip.setTripCosts(0, 0);
            trip.setTime(vals[1]);
            trip.setC02Emissions(Calculate.calculateWalkOrBikeC02Emissions(dist, type, time, Double.parseDouble(arr[7])));
            trip.setCaloriesBurned(Calculate.getMostRecentCalsBurned());
        }

        System.out.println(trip.toString());
        return trip;
    }

    /**
     * Given user input, this method returns a Trip object with all the 
     * necessary output data for air travel.
     * 
     * @param params User input
     * @return Trip object with all relevant output 
     */
    public static Trip runAirplane(String[] params) {
        // Set up and initialize Trip object
        Trip trip = new Trip();
        trip.setAverageMileage(-1);
        trip.setCaloriesBurned(0);
        trip.setTransportType(VehicleType.AIRPLANE);
        trip.setTripCosts(0, 0);
        trip.setC02Emissions(c02EmsFlight);
        String[] tokens = dtMap.get("Flying").split(",");
        if(!tokens[0].equals("N/A")) {
            trip.setDistance(Double.parseDouble(tokens[0]));
        }
        trip.setTime(tokens[1]);
        System.out.println(trip.toString());
        return trip;
    }

    /**
     * Converts the time from hours and minutes to just hours
     * 
     * @param time Time in days, hours and minutes
     * @return Time in hours
     */
    public static double convertTime(String time) {
        Scanner sc = new Scanner(time);
        int hours = 0;
        int days = 0;
        double minutes = 0;
        if(time.contains("days")) {
            days = sc.nextInt();
            sc.next();
        }
        if(time.contains("hours")) {
            hours = sc.nextInt();
            sc.next();
        }
        if(time.contains("mins")) {
            minutes = sc.nextDouble();
            sc.close();
        }
        return days * 24 + hours + minutes / 60.0;
    }
}
