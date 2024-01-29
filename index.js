const cp = require("child_process");
const chokidar = require("chokidar");

const exec = (cmd) => {
  return new Promise((resolve, reject) => {
    const [executable, ...args] = cmd.split(" ");
    const script = cp.spawn(executable, args);
    script.stdout.on("data", (data) => {
      console.log(data.toString());
    });

    script.on("close", (code) => {
      if (code) {
        return reject(code);
      }
      resolve();
    });
  });
};

let IS_RUNNING = false;
chokidar
  .watch(["motor.py"], {
    ignored: [/(^|[\/\\])\../, "dist", "*.egg-info"],
  })
  // .watch(["**/*.py", "*.txt"], {
  //   ignored: [/(^|[\/\\])\../, "dist", "*.egg-info"],
  // })
  .on("all", async () => {
    if (IS_RUNNING) return;
    IS_RUNNING = true;
    const cmd = "./copy-to-remote.sh";
    await exec(cmd);
    IS_RUNNING = false;
  });
