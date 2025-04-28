cmd := exec.Command("git", "fetch", "origin", "HEAD")
     var stderr bytes.Buffer
     cmd.Stderr = &stderr
     err := cmd.Run()
     if err != nil {
         log.Printf("Error: %v, Details: %s", err, stderr.String())
     }