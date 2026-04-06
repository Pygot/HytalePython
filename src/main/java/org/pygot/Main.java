package org.pygot;

import com.hypixel.hytale.logger.HytaleLogger;
import com.hypixel.hytale.server.core.plugin.JavaPlugin;
import com.hypixel.hytale.server.core.plugin.JavaPluginInit;
import com.hypixel.hytale.server.core.universe.world.World;
import com.hypixel.hytale.server.core.universe.Universe;
import org.python.util.PythonInterpreter;

import javax.annotation.Nonnull;
import java.nio.file.*;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.logging.Level;

public final class Main extends JavaPlugin {

    private final JavaPluginInit init;
    public final HytaleLogger Log;

    public Main(@Nonnull JavaPluginInit init) {
        super(init);
        this.init = init;
        Log = getLogger();
    }

    public void runOnMain(Runnable task) {
        World world = Universe.get().getDefaultWorld();

        if (world == null) {
            Log.at(Level.SEVERE).log("Default world not found!");
            return;
        }

        world.execute(task);
    }

    @Override
    protected void start() {
        try {
            Path scriptsDir = getDataDirectory()
                    .toAbsolutePath()
                    .normalize()
                    .resolve("scripts");

            Files.createDirectories(scriptsDir);

            try (DirectoryStream<Path> ds = Files.newDirectoryStream(scriptsDir, "*.py")) {
                for (Path p : ds) {
                    String fileName = p.getFileName().toString();
                    if (!fileName.equals("__init__.py")) {
                        execScript(p, scriptsDir);
                    }
                }
            }

            Log.at(Level.INFO).log("Python runtime started");

        } catch (Throwable t) {
            Log.at(Level.SEVERE).log("Python startup failed - " + t);
        }
    }

    private void execScript(Path file, Path scriptsDir) {
        try {
            PythonInterpreter interp = new PythonInterpreter();

            interp.exec(
                "import sys\n" +
                "p = r'" + scriptsDir.toAbsolutePath().normalize() + "'\n" +
                "if p not in sys.path:\n" +
                "    sys.path.insert(0, p)\n"
            );

            Map<String, Object> exports = new LinkedHashMap<>();
            exports.put("plugin", this);
            exports.put("init", init);

            for (Map.Entry<String, Object> entry : exports.entrySet()) {
                interp.set(entry.getKey(), entry.getValue());
            }

            interp.set("__file__", file.toAbsolutePath().toString());
            interp.execfile(file.toString());
            interp.close();

        } catch (Throwable t) {
            Log.at(Level.SEVERE)
               .log("Python script failed: " + file.getFileName() + " - " + t);
        }
    }

    @Override
    protected void shutdown() {
        Log.at(Level.INFO).log("Python runtime shutdown");
    }
}
