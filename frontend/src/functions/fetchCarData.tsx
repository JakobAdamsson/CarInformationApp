export const fetchCarData = async (registration_number: string, engine_type: string, model: string) => {
    try {
      // Pass the registration_number as part of the URL path
      const response = await fetch(`http://127.0.0.1:5000/vehicle_information/get_data/${registration_number}?Engine=${engine_type}&Model=${model}`, {
        method: 'GET'});
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
      // Assuming the response is JSON
      const data = await response.json();
      return data; // Return or handle the data as needed
    } catch (error) {
      console.error('Error fetching car data:', error);
      throw error; // Or handle the error appropriately
    }
  };
  