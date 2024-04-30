var Fn = {
    // Valida el rut con su cadena completa "XXXXXXXX-X"
    validaRut: function(rutCompleto) {
        if (!/^[0-9]+[-|‐]{1}[0-9kK]{1}$/.test(rutCompleto)) {

            return false;
        }
        
        var tmp = rutCompleto.split('-');
        var digv = tmp[1];
        var rut = tmp[0];
        if (digv == 'K') digv = 'k';
        if (Fn.dv(rut) == digv) {
            // El RUT es válido
            document.getElementById("rutMessage").innerHTML = "El RUT ingresado es válido.";
            return true;
        } else {
            // El RUT es inválido
            document.getElementById("rutMessage").innerHTML = "El RUT ingresado es inválido.";
            return false;
        }
    },
    dv: function(T) {
        var M = 0,
            S = 1;
        for (; T; T = Math.floor(T / 10))
            S = (S + T % 10 * (9 - M++ % 6)) % 11;
        return S ? S - 1 : 'k';
    }
}
