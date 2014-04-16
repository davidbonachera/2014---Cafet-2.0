<?php

    if (isset($_POST['connexion'])) {
            $command =  'python connexion.py -d ' . ' > /dev/null 2>&1 & echo $!; ';
            $pid = exec($command, $output);
            var_dump($pid);
            print 'The PID is: ' . $pid;
    }

    if (isset($_POST['deconnexion'])) {
            $pid = file_get_contents('./saltServer.pid', FILE_USE_INCLUDE_PATH);
            print 'The PID is: ' . $pid;
            exec('kill -USR2 ' . $pid);
    }

    if (isset($_POST['vienoiserieON'])) {
            $pid = file_get_contents('./saltServer.pid', FILE_USE_INCLUDE_PATH);
            print 'The PID is: ' . $pid;
            exec('kill -USR1 ' . $pid);
    }

    if (isset($_POST['vienoiserieOFF'])) {
            $pid = file_get_contents('./saltServer.pid', FILE_USE_INCLUDE_PATH);
            print 'The PID is: ' . $pid;
            exec('kill -INFO ' . $pid);
    }
?>
<html>
<body>
    <form method="post">
	    <p>
		    <button name="connexion">Connexion</button>
			<button name="deconnexion">Déconnexion</button>
			<button name="vienoiserieON">Vienoiserie OK</button>
            <button name="vienoiserieOFF">Vienoiserie Finito</button>
	    </p>
    </form>
</body>