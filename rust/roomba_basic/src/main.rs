extern crate serialport;

use serialport::{SerialPort, SerialPortSettings, DataBits, FlowControl, Parity, StopBits};

const RB_PORT: &str = "COM4";

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("--- Roomba Control via Rust ---");

    let port_settings = SerialPortSettings {
        baud_rate: 115200,
        data_bits: DataBits::Eight,
        flow_control: FlowControl::None,
        parity: Parity::None,
        stop_bits: StopBits::One,
        timeout: std::time::Duration::from_secs(10),
    };

    let mut serial_port = serialport::open_with_settings(&RB_PORT, &port_settings)?;
    let mut stop_flag = true;

    while let Ok(val) = read_input() {
        let speed = 70;
        let speed_rot = 50;

        if !stop_flag {
            println!("STOP MOTOR");
            stop_flag = true;
            drive_pwm(&mut serial_port, 0, 0)?;
        } else {
            match val.as_str() {
                "0" => {
                    println!("ROT-R(0)");
                    stop_flag = false;
                    drive_pwm(&mut serial_port, speed_rot, -speed_rot)?;
                }
                "2" => {
                    println!("ROT-L(2)");
                    stop_flag = false;
                    drive_pwm(&mut serial_port, -speed_rot, speed_rot)?;
                }
                "1" => {
                    println!("FWR(1)");
                    stop_flag = false;
                    drive_pwm(&mut serial_port, speed, speed)?;
                }
                "3" => {
                    println!("BACK(3)");
                    stop_flag = false;
                    drive_pwm(&mut serial_port, -speed, -speed)?;
                }
                "d" => {
                    println!("RESET");
                    stop_flag = true;
                    serial_port.write(&[7])?;
                    let mut str1 = Vec::new();
                    serial_port.read_to_end(&mut str1)?;
                    println!("{:?}", str1);
                }
                "a" => {
                    println!("START");
                    stop_flag = true;
                    let oimode1 = get_oi_mode(&mut serial_port)?;
                    serial_port.write(&[128])?;
                    let oimode2 = get_oi_mode(&mut serial_port)?;
                    println!("OIMode:{}->{}", oimode1, oimode2);
                }
                "g" => {
                    println!("SAFE");
                    stop_flag = true;
                    let oimode1 = get_oi_mode(&mut serial_port)?;
                    serial_port.write(&[131])?;
                    let oimode2 = get_oi_mode(&mut serial_port)?;
                    println!("OIMode:{}->{}", oimode1, oimode2);
                }
                "f" => {
                    println!("FULL");
                    stop_flag = true;
                    let oimode1 = get_oi_mode(&mut serial_port)?;
                    serial_port.write(&[132])?;
                    let oimode2 = get_oi_mode(&mut serial_port)?;
                    println!("OIMode:{}->{}", oimode1, oimode2);
                }
                "w" => {
                    println!("DOCK");
                    serial_port.write(&[143])?;
                }
                "z" => {
                    println!("SENSOR");
                    let (el, er) = get_encs(&mut serial_port)?;
                    let oimode = get_oi_mode(&mut serial_port)?;
                    let vol = get_sensor(&mut serial_port, 22, 2, false)?;
                    let cur = get_sensor(&mut serial_port, 23, 2, false)?;

                    println!("Enc L:{} R:{}", el, er);
                    println!("OIMode:{}", oimode);
                    println!("Voltage/Current = {}[mV]/{}[mA]", vol, cur);
                }
                _ => println!("Input val={}", val),
            }
        }
    }

    Ok(())
}

fn read_input() -> Result<String, std::io::Error> {
    let mut input = String::new();
    std::io::stdin().read_line(&mut input)?;
    Ok(input.trim().to_string())
}

fn drive_pwm(port: &mut Box<dyn SerialPort>, l_pwm: i16, r_pwm: i16) -> Result<(), std::io::Error> {
    let l_hb = (l_pwm >> 8) as u8;
    let l_lb = (l_pwm & 0x00FF) as u8;
    let r_hb = (r_pwm >> 8) as u8;
    let r_lb = (r_pwm & 0x00FF) as u8;

    port.write(&[146, r_hb, r_lb, l_hb, l_lb])?;
    Ok(())
}

fn get_sensor(port: &mut Box<dyn SerialPort>, p_id: u8, len: usize, sign_flg: bool) -> Result<i16, std::io::Error> {
    port.write(&[142, p_id])?;
    let mut data = vec![0u8; len];
    port.read_exact(&mut data)?;

    let data_slice: [u8; 2] = data.as_slice().try_into().unwrap();
    let value = i16::from_be_bytes(data_slice) >> (if sign_flg { 0 } else { 8 });
    Ok(value)
}

fn get_encs(port: &mut Box<dyn SerialPort>) -> Result<(i16, i16), std::io::Error> {
    let enc_l = get_sensor(port, 43, 2, false)?;
    let enc_r = get_sensor(port, 44, 2, false)?;
    Ok((enc_l, enc_r))
}

fn get_oi_mode(port: &mut Box<dyn SerialPort>) -> Result<u8, std::io::Error> {
    let oi_mode = get_sensor(port, 35, 1, false)?;
    Ok(oi_mode as u8)
}
