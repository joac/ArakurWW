$(document).ready(function(){  
    first_load = true;  

    function update(state){
        //Instrumentos
        var actual_program = state.programs[state.params.programa_actual - 1];

        update_bar("turbiedad", state.instant_values.cloudiness, "NTU", 30); 
        update_bar("nivel", state.instant_values.level, "%");   
        update_bar("oxigeno", state.instant_values.oxigen, "mg/Litro", 20);
        //Volumenes
        update_tag("volumen_tratado", state.instant_values.volumen_tratado, 'm³');
        update_tag("volumen_tratado_parcial", state.instant_values.volumen_tratado_parcial, 'm³');
        //Progreso
        update_tag("programa_actual", state.params.programa_actual);
        var process_times = ['carga_aireada', 'sedimentacion', 'descarga', 'aireacion'];
    
        for(var n=0; n<process_times.length; n++){
            var tag = process_times[n];
            update_tag("programa_" + tag, actual_program[tag], 'minutos');
            update_bar(tag, state.instant_values[tag], 'minutos', actual_program[tag]);
        }; 

        if (first_load){
            for(var i = 0; i < state.alarms.length; i++){
                var alarm = state.alarms[i];
                set_alert(alarm.text, alarm.time);                
                };
            for(var i = 0; i < state.events.length; i++){
                var evt = state.events[i];
                set_notify(evt.text, evt.time);                
                };
            first_load = false;
        } else {
            for(var i = 0; i < state.new_alarms.length; i++){
                var alarm = state.new_alarms[i];
                set_alert(alarm.text, alarm.time);                
            }; 
            for(var i = 0; i < state.new_events.length; i++){
                var evt = state.new_events[i];
                set_notify(evt.text, evt.time);                
            };
}; 
    };
    state_handler(update);
});

